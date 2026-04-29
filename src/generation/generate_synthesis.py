"""Tenacious-Bench synthetic task generation with committed prompts and judge filtering."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import (
    REPO_ROOT,
    append_cost_log,
    prompt_manifest_path,
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


SYNTHESIS_SPECS: list[dict[str, Any]] = [
    {
        "task_id_stub": "synthetic-signal-grounding",
        "focus": "Generate one cold-outreach email task where weak public signal must stay interrogative rather than assertive.",
        "probe_id": "P05",
        "failure_dimension": "signal_grounding",
        "message_kind": "cold_outreach",
    },
    {
        "task_id_stub": "synthetic-gap-condescension",
        "focus": "Generate one Segment 4 email task where competitor-gap evidence must be framed as research, not buyer failure.",
        "probe_id": "P33",
        "failure_dimension": "gap_condescension",
        "message_kind": "cold_outreach",
    },
    {
        "task_id_stub": "synthetic-fixture-boundary",
        "focus": "Generate one warm-reply task where a demo artifact must be described honestly as demo-mode, not production.",
        "probe_id": "P30",
        "failure_dimension": "style_guide_adherence",
        "message_kind": "warm_reply",
    },
]

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic Tenacious-Bench tasks or prompt manifests.")
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "tenacious_bench_v0.1" / "dev" / "synthetic_tasks.jsonl",
        help="Where to write schema-valid synthetic tasks.",
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
    return parser.parse_args()


def build_prompt_manifest(partition: str, generation_model: str, judge_model: str) -> list[dict[str, Any]]:
    manifest = []
    for index, spec in enumerate(SYNTHESIS_SPECS, start=1):
        manifest.append(
            {
                "id": f"{partition}-synthetic-{index:03d}-{spec['task_id_stub']}",
                "prompt_version": PROMPT_VERSION,
                "model_role": "bulk_variation_generation",
                "generation_model": generation_model,
                "judge_model": judge_model,
                "probe_id": spec["probe_id"],
                "failure_dimension": spec["failure_dimension"],
                "system_prompt": SYSTEM_PROMPT,
                "user_prompt": build_generation_prompt(spec, index, partition),
                "judge_system_prompt": JUDGE_SYSTEM_PROMPT,
            }
        )
    return manifest


def judge_candidate(client: OpenAI, judge_model: str, task: dict[str, Any]) -> dict[str, Any]:
    response = client.chat.completions.create(
        model=judge_model,
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


def generate_live_tasks(model: str, judge_model: str, partition: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is required for live synthesis mode.")
    enforce_rotation(model, judge_model)

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    tasks: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for index, spec in enumerate(SYNTHESIS_SPECS, start=1):
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_generation_prompt(spec, index, partition)},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or ""
        try:
            task = json.loads(content)
            task["partition"] = partition
            task["source_mode"] = "synthetic"
            task.setdefault("metadata", {})
            task["metadata"]["prompt_version"] = PROMPT_VERSION
            task["metadata"]["generation_model"] = model
            task["metadata"]["judge_model"] = judge_model
            validate_task(task)
            judgment = judge_candidate(client, judge_model, task)
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
    manifest = build_prompt_manifest(args.partition, args.model, args.judge_model)
    write_jsonl(prompt_manifest_path(args.output), manifest)

    if not args.live:
        print(
            json.dumps(
                {
                    "mode": "offline",
                    "prompt_manifest": str(prompt_manifest_path(args.output)),
                    "prompt_count": len(manifest),
                    "prompt_version": PROMPT_VERSION,
                    "generation_model": args.model,
                    "judge_model": args.judge_model,
                },
                indent=2,
            )
        )
        return 0

    tasks, skipped = generate_live_tasks(args.model, args.judge_model, args.partition)
    write_jsonl(args.output, tasks)
    if skipped:
        skip_path = args.output.with_name(args.output.stem + "_judge_rejections.json")
        skip_path.write_text(json.dumps(skipped, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "mode": "live",
                "output_path": str(args.output),
                "task_count": len(tasks),
                "task_ids": [task["task_id"] for task in tasks],
                "rejected_count": len(skipped),
                "prompt_version": PROMPT_VERSION,
                "generation_model": args.model,
                "judge_model": args.judge_model,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
