"""Generate model predictions for held-out tasks.

Modes
-----
  --mode trained      base model + LoRA adapter (ORPO-tuned critic)
  --mode prompt_only  bare base model, no adapter

Both modes format each held-out task as the same prompt used during ORPO
training, run inference, parse the Subject/Body output, and write a JSONL
file that run_ablation.py accepts as --trained-predictions or
--prompt-only-predictions.

Usage
-----
  python src/ablations/generate_model_predictions.py --mode trained
  python src/ablations/generate_model_predictions.py --mode prompt_only

  # Custom paths:
  python src/ablations/generate_model_predictions.py \\
      --mode trained \\
      --adapter-path models/orpo_qwen3_0_6b_lora_adapter \\
      --output reports/trained_predictions.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
HELD_OUT_DIR = REPO_ROOT / "tenacious_bench_v0.1" / "held_out"
DEFAULT_ADAPTER_PATH = REPO_ROOT / "models" / "orpo_qwen3_0_6b_lora_adapter"
DEFAULT_BASE_MODEL = "unsloth/Qwen3-0.6B"
MAX_NEW_TOKENS = 300


# ---------------------------------------------------------------------------
# Prompt construction — mirrors the format used in ORPO training data.
# ---------------------------------------------------------------------------

def _signals_text(brief: dict[str, Any]) -> str:
    lines = []
    for sig in brief.get("signals", []):
        if isinstance(sig, dict):
            stype = sig.get("signal_type", "signal")
            conf = sig.get("confidence", "medium")
            text = sig.get("evidence") or sig.get("signal_type", "")
        else:
            stype, conf, text = "signal", "medium", str(sig)
        lines.append(f"- {stype} ({conf}): {text}")
    return "\n".join(lines) if lines else "- no signals provided"


def build_prompt(task: dict[str, Any]) -> str:
    inp = task.get("input", {})
    prospect = inp.get("prospect", {})
    brief = inp.get("hiring_signal_brief", {})
    prior = inp.get("prior_thread", {})
    rubric = task.get("rubric", {})
    sc = task.get("scoring_config", {})
    gt = task.get("ground_truth", {})

    channel = task.get("channel", "email")
    message_kind = task.get("message_kind", "cold_outreach")
    company_name = prospect.get("company_name", "Unknown")
    contact_role = prospect.get("contact_role", "")
    company_stage = prospect.get("company_stage", "")
    failure_dim = task.get("failure_dimension", "")
    judge_dims = ", ".join(sc.get("judge_dimensions", []))
    prior_summary = prior.get("summary", "No prior contact.")
    expected_behavior = gt.get("expected_behavior", "")
    required = ", ".join(rubric.get("expected_terms", []))
    forbidden = ", ".join(rubric.get("forbidden_terms", []))
    banned = ", ".join(rubric.get("banned_phrases", []))

    return (
        f"Write a {channel} {message_kind} for {contact_role} at {company_name} ({company_stage}).\n"
        f"Failure dimension focus: {failure_dim}.\n"
        f"Judge dimensions: {judge_dims}.\n"
        f"Prior thread summary: {prior_summary}\n"
        f"Signals:\n{_signals_text(brief)}\n"
        f"Expected behavior: {expected_behavior}\n"
        f"Required terms: {required}\n"
        f"Forbidden terms: {forbidden}\n"
        f"Banned phrases: {banned}\n"
        "Keep the response grounded, professional, and limited to one buyer-facing next step."
    )


# ---------------------------------------------------------------------------
# Output parsing — expects "Subject: ...\nBody: ..." format.
# ---------------------------------------------------------------------------

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_SUBJECT_RE = re.compile(r"(?i)^subject:\s*(.+)", re.MULTILINE)
_BODY_RE = re.compile(r"(?i)^body:\s*([\s\S]+)", re.MULTILINE)


def parse_output(raw: str) -> dict[str, str]:
    text = _THINK_RE.sub("", raw).strip()
    subject_m = _SUBJECT_RE.search(text)
    body_m = _BODY_RE.search(text)
    subject = subject_m.group(1).strip() if subject_m else ""
    body = body_m.group(1).strip() if body_m else text
    # Trim trailing assistant artifacts.
    body = body.split("<|im_end|>")[0].split("<|endoftext|>")[0].strip()
    return {"subject": subject, "body": body}


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_model_and_tokenizer(mode: str, adapter_path: Path, base_model: str) -> tuple[Any, Any]:
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError:
        print("transformers and torch are required. pip install transformers torch", file=sys.stderr)
        raise

    print(f"Loading tokenizer from {base_model} ...")
    tokenizer = AutoModelForCausalLM  # placeholder until below
    tokenizer = __import__("transformers").AutoTokenizer.from_pretrained(
        base_model, trust_remote_code=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    device_map = "auto" if torch.cuda.is_available() else "cpu"
    print(f"Loading base model {base_model} (dtype={dtype}, device={device_map}) ...")
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=dtype,
        device_map=device_map,
        trust_remote_code=True,
    )

    if mode == "trained":
        try:
            from peft import PeftModel
        except ImportError:
            print("peft is required for trained mode. pip install peft", file=sys.stderr)
            raise
        print(f"Attaching LoRA adapter from {adapter_path} ...")
        model = PeftModel.from_pretrained(model, str(adapter_path))
        model = model.merge_and_unload()

    model.eval()
    return model, tokenizer


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------

def run_inference(model: Any, tokenizer: Any, prompt: str) -> tuple[str, float]:
    import torch

    messages = [{"role": "user", "content": prompt}]
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
    )
    device = next(model.parameters()).device
    input_ids = input_ids.to(device)

    t0 = time.monotonic()
    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    latency_ms = (time.monotonic() - t0) * 1000

    new_tokens = output_ids[0][input_ids.shape[-1]:]
    raw = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return raw, latency_ms


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_tasks() -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for path in sorted(HELD_OUT_DIR.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    return tasks


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate model predictions for held-out tasks.")
    parser.add_argument(
        "--mode",
        choices=("trained", "prompt_only"),
        required=True,
        help="trained: base + LoRA adapter. prompt_only: bare base model.",
    )
    parser.add_argument(
        "--adapter-path",
        type=Path,
        default=DEFAULT_ADAPTER_PATH,
        help="Path to LoRA adapter directory (trained mode only).",
    )
    parser.add_argument(
        "--base-model",
        default=DEFAULT_BASE_MODEL,
        help="HuggingFace model ID or local path for the base model.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output JSONL path. Defaults to reports/{mode}_predictions.jsonl.",
    )
    parser.add_argument(
        "--held-out-dir",
        type=Path,
        default=HELD_OUT_DIR,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = args.output or (REPO_ROOT / "reports" / f"{args.mode}_predictions.jsonl")

    tasks = load_tasks()
    print(f"Loaded {len(tasks)} held-out tasks")

    model, tokenizer = load_model_and_tokenizer(args.mode, args.adapter_path, args.base_model)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    written = skipped = 0

    with output_path.open("w", encoding="utf-8") as fh:
        for i, task in enumerate(tasks, 1):
            task_id = task.get("task_id", f"task_{i}")
            prompt = build_prompt(task)
            try:
                raw, latency_ms = run_inference(model, tokenizer, prompt)
                candidate = parse_output(raw)
            except Exception as exc:
                print(f"  SKIP {task_id}: {type(exc).__name__}: {exc}", file=sys.stderr)
                skipped += 1
                continue

            row = {
                "task_id": task_id,
                "candidate_output": candidate,
                "latency_ms": round(latency_ms, 1),
                "input_tokens": 0,
                "output_tokens": 0,
                "usd_cost": 0.0,
            }
            fh.write(json.dumps(row) + "\n")
            written += 1
            if i % 10 == 0:
                print(f"  {i}/{len(tasks)} done")

    print(f"Done - wrote {written} predictions, skipped {skipped} -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
