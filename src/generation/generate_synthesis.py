"""Tenacious-Bench synthetic task generation with committed prompts and judge filtering."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import TYPE_CHECKING, Any

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional for offline manifest generation
    load_dotenv = None

try:
    from openai import OpenAI, RateLimitError
    OPENAI_AVAILABLE = True
except ImportError:  # pragma: no cover - optional for offline manifest generation
    OPENAI_AVAILABLE = False
    OpenAI = Any  # type: ignore[assignment]

    class RateLimitError(Exception):
        """Fallback used when the OpenAI package is not installed."""


if TYPE_CHECKING:
    from openai import OpenAI as OpenAIClient

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import (
    REPO_ROOT,
    append_cost_log,
    prompt_manifest_path,
    read_jsonl,
    validate_task,
    write_jsonl,
)
from src.generation.synthesis_policy import (
    DEFAULT_GENERATION_MODEL,
    DEFAULT_JUDGE_MODEL,
    JUDGE_SYSTEM_PROMPT,
    PROMPT_VERSION,
    SYSTEM_PROMPT,
    build_generation_prompt,
    build_judge_prompt,
    enforce_rotation,
)

DEFAULT_SEED = 11


SYNTHESIS_SPECS: list[dict[str, Any]] = [
    # ── Original dev specs ───────────────────────────────────────────────────
    {
        "task_id_stub": "synthetic-signal-grounding",
        "focus": "Generate one cold-outreach email task where weak public signal must stay interrogative rather than assertive.",
        "probe_id": "P05",
        "failure_dimension": "signal_grounding",
        "message_kind": "cold_outreach",
        "partitions": ["dev"],
    },
    {
        "task_id_stub": "synthetic-gap-condescension",
        "focus": "Generate one Segment 4 email task where competitor-gap evidence must be framed as research, not buyer failure.",
        "probe_id": "P33",
        "failure_dimension": "gap_condescension",
        "message_kind": "cold_outreach",
        "partitions": ["dev"],
    },
    {
        "task_id_stub": "synthetic-fixture-boundary",
        "focus": "Generate one warm-reply task where a demo artifact must be described honestly as demo-mode, not production.",
        "probe_id": "P30",
        "failure_dimension": "style_guide_adherence",
        "message_kind": "warm_reply",
        "partitions": ["dev"],
    },
    # ── Gap-fill: signal_grounding — train (4 specs) ─────────────────────────
    {
        "task_id_stub": "synthetic-signal-grounding-stale-press",
        "focus": (
            "Generate one cold-outreach email where the only public signal is a 14-month-old press release. "
            "The sender must cite it as stale and ask a grounding question rather than asserting intent."
        ),
        "probe_id": "P07",
        "failure_dimension": "signal_grounding",
        "message_kind": "cold_outreach",
        "partitions": ["train"],
    },
    {
        "task_id_stub": "synthetic-signal-grounding-unverified-headcount",
        "focus": (
            "Generate one warm-reply email where the sender previously cited a headcount figure sourced from "
            "a third-party aggregator rather than a public filing. The reply must retract the figure and ask "
            "the buyer to confirm actual team size."
        ),
        "probe_id": "P03",
        "failure_dimension": "signal_grounding",
        "message_kind": "warm_reply",
        "partitions": ["train"],
    },
    {
        "task_id_stub": "synthetic-signal-grounding-conflicting-job-posts",
        "focus": (
            "Generate one cold-outreach email where two public signals conflict: a job post for 'data engineer' "
            "and a separate post for 'data platform deprecation'. The sender must flag the conflict and not assert "
            "a hiring direction."
        ),
        "probe_id": "P05",
        "failure_dimension": "signal_grounding",
        "message_kind": "cold_outreach",
        "partitions": ["train"],
    },
    {
        "task_id_stub": "synthetic-signal-grounding-zero-public-signal",
        "focus": (
            "Generate one cold-outreach email for a prospect with no verifiable public hiring or technology "
            "signal. The sender must abstain from any capability or intent claim and ground the ask entirely "
            "in a question about current state."
        ),
        "probe_id": "P29",
        "failure_dimension": "signal_grounding",
        "message_kind": "cold_outreach",
        "partitions": ["train"],
    },
    # ── Gap-fill: next_step_quality — train (3 specs) ────────────────────────
    {
        "task_id_stub": "synthetic-next-step-vague-cta",
        "focus": (
            "Generate one warm-reply email where the candidate output avoids vague CTAs like 'let me know if "
            "interested' and instead asks one specific, answerable question about a named operational area."
        ),
        "probe_id": "P34",
        "failure_dimension": "next_step_quality",
        "message_kind": "warm_reply",
        "partitions": ["train"],
    },
    {
        "task_id_stub": "synthetic-next-step-timeline-before-gate",
        "focus": (
            "Generate one cold-outreach email where the buyer has asked for a delivery timeline before the "
            "capacity gate has been cleared. The sender must decline to quote a timeline and redirect to the "
            "capacity question."
        ),
        "probe_id": "P31",
        "failure_dimension": "next_step_quality",
        "message_kind": "cold_outreach",
        "partitions": ["train"],
    },
    {
        "task_id_stub": "synthetic-next-step-bundled-asks",
        "focus": (
            "Generate one warm-reply email where the candidate output contains exactly one ask, despite the "
            "context giving multiple natural follow-up directions. The sender must choose the highest-signal "
            "single question and defer the rest."
        ),
        "probe_id": "P35",
        "failure_dimension": "next_step_quality",
        "message_kind": "warm_reply",
        "partitions": ["train"],
    },
    # ── Gap-fill: signal_grounding — dev (2 specs) ───────────────────────────
    {
        "task_id_stub": "synthetic-signal-grounding-low-confidence-flag",
        "focus": (
            "Generate one cold-outreach email where the signal confidence is explicitly low. The sender must "
            "flag the low confidence in-line and frame the ask as hypothesis-testing rather than confirming "
            "a belief."
        ),
        "probe_id": "P05",
        "failure_dimension": "signal_grounding",
        "message_kind": "cold_outreach",
        "partitions": ["dev"],
    },
    {
        "task_id_stub": "synthetic-signal-grounding-paraphrase-retraction",
        "focus": (
            "Generate one warm-reply email where the sender must retract a capability claim made in a prior "
            "note because the source was a press paraphrase not a verified filing. The retraction must be "
            "direct and replace the claim with a grounding question."
        ),
        "probe_id": "P03",
        "failure_dimension": "signal_grounding",
        "message_kind": "warm_reply",
        "partitions": ["dev"],
    },
    # ── Gap-fill: next_step_quality — dev (2 specs) ──────────────────────────
    {
        "task_id_stub": "synthetic-next-step-calendar-blocked",
        "focus": (
            "Generate one warm-reply email where the prospect explicitly stated in a prior thread that they "
            "do not want calendar invites. The CTA must be a reply-based question, not a booking link or "
            "meeting suggestion."
        ),
        "probe_id": "P34",
        "failure_dimension": "next_step_quality",
        "message_kind": "warm_reply",
        "partitions": ["dev"],
    },
    {
        "task_id_stub": "synthetic-next-step-premature-scoping",
        "focus": (
            "Generate one cold-outreach email where the buyer's prior question asked for a scoping estimate "
            "before a fit check has been done. The sender must decline the estimate and redirect to the fit "
            "question first."
        ),
        "probe_id": "P31",
        "failure_dimension": "next_step_quality",
        "message_kind": "cold_outreach",
        "partitions": ["dev"],
    },
]

def _partition_specs(partition: str) -> list[dict[str, Any]]:
    return [s for s in SYNTHESIS_SPECS if partition in s.get("partitions", [partition])]


def _normalize_text(value: str) -> str:
    collapsed = re.sub(r"\s+", " ", value.strip().lower())
    return re.sub(r"[^a-z0-9 ]+", "", collapsed)


def dedup_key(task: dict[str, Any]) -> tuple[str, str, str, str, str]:
    candidate_output = task.get("candidate_output", {})
    return (
        str(task.get("failure_dimension", "")).strip().lower(),
        str(task.get("channel", "")).strip().lower(),
        str(task.get("message_kind", "")).strip().lower(),
        _normalize_text(str(candidate_output.get("subject", ""))),
        _normalize_text(str(candidate_output.get("body", ""))),
    )


def _task_id(task: dict[str, Any]) -> str:
    return str(task.get("task_id", "")).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic Tenacious-Bench tasks or prompt manifests.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Where to write schema-valid synthetic tasks (default: tenacious_bench_v0.1/<partition>/synthetic_tasks.jsonl).",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Call the configured OpenRouter model instead of writing only a prompt manifest.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_GENERATION_MODEL,
        help="OpenRouter model name to use for generation in live mode.",
    )
    parser.add_argument(
        "--judge-model",
        default=DEFAULT_JUDGE_MODEL,
        help="OpenRouter model name to use for synthesis judge filtering in live mode.",
    )
    parser.add_argument(
        "--partition",
        choices=("train", "dev", "held_out"),
        default="dev",
        help="Partition label to stamp onto the generated tasks.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Base seed for live generation and judge calls. Incremented per synthesis spec.",
    )
    return parser.parse_args()


def build_prompt_manifest(
    partition: str,
    generation_model: str,
    judge_model: str,
    seed: int,
) -> list[dict[str, Any]]:
    manifest = []
    for index, spec in enumerate(_partition_specs(partition), start=1):
        spec_seed = seed + index - 1
        manifest.append(
            {
                "id": f"{partition}-synthetic-{index:03d}-{spec['task_id_stub']}",
                "prompt_version": PROMPT_VERSION,
                "model_role": "bulk_variation_generation",
                "generation_model": generation_model,
                "judge_model": judge_model,
                "generation_seed": spec_seed,
                "probe_id": spec["probe_id"],
                "failure_dimension": spec["failure_dimension"],
                "system_prompt": SYSTEM_PROMPT,
                "user_prompt": build_generation_prompt(spec, index, partition),
                "judge_system_prompt": JUDGE_SYSTEM_PROMPT,
            }
        )
    return manifest


def judge_candidate(
    client: "OpenAIClient",
    judge_model: str,
    task: dict[str, Any],
    seed: int,
    retries: int = 2,
) -> dict[str, Any]:
    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model=judge_model,
                seed=seed,
                temperature=0,
                messages=[
                    {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                    {"role": "user", "content": build_judge_prompt(task)},
                ],
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or ""
            judgment = json.loads(content)
            if judgment.get("decision") not in {"accept", "revise", "block"}:
                raise ValueError(f"Unexpected judge decision payload: {judgment}")
            return judgment
        except RateLimitError:
            if attempt == retries:
                raise
            time.sleep(15 * (attempt + 1))


def generate_live_tasks(
    model: str,
    judge_model: str,
    partition: str,
    output: Path,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if load_dotenv is not None:
        load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is required for live synthesis mode.")
    if not OPENAI_AVAILABLE:
        raise RuntimeError("The openai package is required for live synthesis mode.")
    enforce_rotation(model, judge_model)

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    existing_rows = read_jsonl(output)
    seen_task_ids = {_task_id(row) for row in existing_rows if _task_id(row)}
    seen_dedup_keys = {dedup_key(row) for row in existing_rows}
    tasks: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for index, spec in enumerate(_partition_specs(partition), start=1):
        spec_seed = seed + index - 1
        for gen_attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=model,
                    seed=spec_seed,
                    temperature=0,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": build_generation_prompt(spec, index, partition)},
                    ],
                    response_format={"type": "json_object"},
                )
                break
            except RateLimitError:
                if gen_attempt == 2:
                    raise
                time.sleep(15 * (gen_attempt + 1))
        content = response.choices[0].message.content or ""
        try:
            task = json.loads(content)
            task["partition"] = partition
            task["source_mode"] = "synthetic"
            task.setdefault("metadata", {})
            task["metadata"]["prompt_version"] = PROMPT_VERSION
            task["metadata"]["generation_model"] = model
            task["metadata"]["judge_model"] = judge_model
            task["metadata"]["generation_seed"] = spec_seed
            task["metadata"]["judge_seed"] = spec_seed
            validate_task(task)
            task_id = _task_id(task)
            if task_id and task_id in seen_task_ids:
                skipped.append(
                    {
                        "id": task_id,
                        "reason": "duplicate_task_id",
                    }
                )
                continue
            task_key = dedup_key(task)
            if task_key in seen_dedup_keys:
                skipped.append(
                    {
                        "id": task_id or f"{partition}-synthetic-{index:03d}-{spec['task_id_stub']}",
                        "reason": "duplicate_candidate_output",
                    }
                )
                continue
            judgment = judge_candidate(client, judge_model, task, spec_seed)
        except (json.JSONDecodeError, ValueError) as exc:
            skipped.append(
                {
                    "id": f"{partition}-synthetic-{index:03d}-{spec['task_id_stub']}",
                    "reason": str(exc),
                }
            )
            continue
        if judgment["decision"] != "accept":
            skipped.append(
                {
                    "id": task.get("task_id", f"{partition}-synthetic-{index:03d}-{spec['task_id_stub']}"),
                    "reason": "judge_rejected",
                    "judgment": judgment,
                }
            )
            continue
        task["metadata"]["judge_confidence"] = judgment.get("confidence", "")
        task["metadata"]["judge_reasons"] = judgment.get("reasons", [])
        tasks.append(task)
        if task_id:
            seen_task_ids.add(task_id)
        seen_dedup_keys.add(task_key)
        append_cost_log(
            bucket="dataset_authoring",
            provider="OpenRouter",
            model_or_compute=f"{model} -> {judge_model}",
            purpose=f"synthetic_generation_and_judge_filter:{task.get('task_id', '')}",
            estimated_cost_usd=0.0,
            actual_cost_usd=0.0,
            notes="Live synthesis call completed; cost fields left zero until provider usage export is available.",
        )
    return tasks, skipped


def main() -> int:
    args = parse_args()
    output = args.output or (
        REPO_ROOT / "tenacious_bench_v0.1" / args.partition / "synthetic_tasks.jsonl"
    )
    manifest = build_prompt_manifest(args.partition, args.model, args.judge_model, args.seed)
    write_jsonl(prompt_manifest_path(output), manifest)

    if not args.live:
        print(
            json.dumps(
                {
                    "mode": "offline",
                    "partition": args.partition,
                    "spec_count": len(_partition_specs(args.partition)),
                    "prompt_manifest": str(prompt_manifest_path(output)),
                    "prompt_count": len(manifest),
                    "prompt_version": PROMPT_VERSION,
                    "generation_model": args.model,
                    "judge_model": args.judge_model,
                    "seed": args.seed,
                },
                indent=2,
            )
        )
        return 0

    existing_rows = read_jsonl(output)
    tasks, skipped = generate_live_tasks(args.model, args.judge_model, args.partition, output, args.seed)
    write_jsonl(output, [*existing_rows, *tasks])
    if skipped:
        skip_path = output.with_name(output.stem + "_judge_rejections.json")
        skip_path.write_text(json.dumps(skipped, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "mode": "live",
                "partition": args.partition,
                "output_path": str(output),
                "task_count": len(existing_rows) + len(tasks),
                "new_task_count": len(tasks),
                "task_ids": [task["task_id"] for task in tasks],
                "rejected_count": len(skipped),
                "prompt_version": PROMPT_VERSION,
                "generation_model": args.model,
                "judge_model": args.judge_model,
                "seed": args.seed,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
