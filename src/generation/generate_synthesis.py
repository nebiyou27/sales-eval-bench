"""Scaffold Tenacious-Bench synthetic task generation.

Default mode writes a prompt manifest for later review. Optional live mode sends
the prompts to an OpenRouter-compatible chat model and validates returned tasks.
"""

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
    prompt_manifest_path,
    validate_task,
    write_jsonl,
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


SYSTEM_PROMPT = """You are authoring Tenacious-Bench v0.1 benchmark tasks.
Return exactly one JSON object matching the local schema for each request.
The task must:
- be Tenacious-specific B2B sales work, not generic retail
- use channel=email
- use subject/body output format
- keep one ask only
- preserve Tenacious style markers: direct, grounded, honest, professional, non-condescending where relevant
- include metadata.style_guide_version=\"v2\"
- include metadata.retrieval_provenance when source_mode=synthetic and failure_dimension=signal_grounding
- set ground_truth.target_decision to accept, revise, or block
- use source_mode=synthetic
Do not wrap the JSON in markdown fences."""


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
        default="qwen/qwen3-next-80b-a3b-instruct",
        help="OpenRouter model name to use in live mode.",
    )
    return parser.parse_args()


def build_user_prompt(spec: dict[str, Any], index: int) -> str:
    return f"""Create one schema-valid Tenacious-Bench task.
Task id stem: dev-{index:03d}-{spec['task_id_stub']}
Focus: {spec['focus']}
Probe ID: {spec['probe_id']}
Failure dimension: {spec['failure_dimension']}
Message kind: {spec['message_kind']}
Partition: dev
Use the current schema fields and include explicit signal evidence, bench context, prior thread context, and a strict rubric.
The candidate output should be realistic outreach, not a placeholder."""


def build_prompt_manifest() -> list[dict[str, Any]]:
    manifest = []
    for index, spec in enumerate(SYNTHESIS_SPECS, start=1):
        manifest.append(
            {
                "id": f"dev-{index:03d}-{spec['task_id_stub']}",
                "model_role": "bulk_variation_generation",
                "probe_id": spec["probe_id"],
                "failure_dimension": spec["failure_dimension"],
                "system_prompt": SYSTEM_PROMPT,
                "user_prompt": build_user_prompt(spec, index),
            }
        )
    return manifest


def generate_live_tasks(model: str) -> list[dict[str, Any]]:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is required for live synthesis mode.")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    tasks: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for index, spec in enumerate(SYNTHESIS_SPECS, start=1):
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(spec, index)},
            ],
        )
        content = response.choices[0].message.content or ""
        try:
            task = json.loads(content)
            validate_task(task)
        except (json.JSONDecodeError, ValueError) as exc:
            skipped.append(
                {
                    "id": f"dev-{index:03d}-{spec['task_id_stub']}",
                    "reason": str(exc),
                }
            )
            continue
        tasks.append(task)
    if skipped:
        skip_path = REPO_ROOT / "tenacious_bench_v0.1" / "dev" / "synthetic_tasks_skipped.json"
        skip_path.write_text(json.dumps(skipped, indent=2), encoding="utf-8")
    return tasks


def main() -> int:
    args = parse_args()
    manifest = build_prompt_manifest()
    write_jsonl(prompt_manifest_path(args.output), manifest)

    if not args.live:
        print(
            json.dumps(
                {
                    "mode": "offline",
                    "prompt_manifest": str(prompt_manifest_path(args.output)),
                    "prompt_count": len(manifest),
                },
                indent=2,
            )
        )
        return 0

    tasks = generate_live_tasks(args.model)
    write_jsonl(args.output, tasks)
    print(
        json.dumps(
            {
                "mode": "live",
                "output_path": str(args.output),
                "task_count": len(tasks),
                "task_ids": [task["task_id"] for task in tasks],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
