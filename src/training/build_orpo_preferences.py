"""Build ORPO preference pairs from public Tenacious-Bench tasks only."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import REPO_ROOT, read_jsonl, write_jsonl
from src.training.prepare_orpo_data import prepare_records


DATASET_ROOT = REPO_ROOT / "tenacious_bench_v0.1"
OUTPUT_PATH = REPO_ROOT / "training_data" / "orpo_preferences.jsonl"
PUBLIC_PARTITIONS = ("train", "dev")
DEFAULT_CHOSEN_REWRITE_MODEL = "qwen/qwen3-next-80b-a3b-instruct"
DEFAULT_JUDGE_MODEL = "deepseek/deepseek-chat"
LOCAL_REJECTED_MODEL = "local/rule_based_variant"
ROW_REQUIRED_FIELDS = (
    "source_task_id",
    "source_partition",
    "failure_dimension",
    "prompt",
    "chosen",
    "rejected",
    "chosen_source",
    "rejected_source",
    "rejected_model",
    "metadata",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build public-only ORPO preference pairs.")
    parser.add_argument("--dataset-root", type=Path, default=DATASET_ROOT)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--chosen-rewrite-model", default=DEFAULT_CHOSEN_REWRITE_MODEL)
    parser.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_public_tasks(dataset_root: Path) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for partition in PUBLIC_PARTITIONS:
        partition_dir = dataset_root / partition
        if not partition_dir.exists():
            continue
        for path in sorted(partition_dir.glob("*.jsonl")):
            for row in read_jsonl(path):
                if row.get("partition") != partition:
                    continue
                if "task_id" not in row or "candidate_output" not in row:
                    continue
                tasks.append(row)
    return tasks


def format_candidate_output(candidate_output: Any) -> str:
    if isinstance(candidate_output, dict):
        subject = candidate_output.get("subject")
        body = candidate_output.get("body")
        parts: list[str] = []
        if isinstance(subject, str) and subject.strip():
            parts.append(f"Subject: {subject.strip()}")
        if isinstance(body, str) and body.strip():
            parts.append(f"Body: {body.strip()}")
        if parts:
            return "\n".join(parts)
    if isinstance(candidate_output, str):
        return candidate_output.strip()
    return json.dumps(candidate_output, ensure_ascii=True, sort_keys=True)


def render_signal_summary(task: dict[str, Any]) -> str:
    signals = task.get("input", {}).get("hiring_signal_brief", {}).get("signals", [])
    rendered: list[str] = []
    for signal in signals:
        signal_type = signal.get("signal_type", "signal")
        evidence = signal.get("evidence", "")
        confidence = signal.get("confidence", "")
        rendered.append(f"- {signal_type} ({confidence}): {evidence}".strip())
    return "\n".join(rendered) if rendered else "- no explicit signal captured"


def render_prompt(task: dict[str, Any]) -> str:
    prospect = task.get("input", {}).get("prospect", {})
    prior_thread = task.get("input", {}).get("prior_thread", {})
    rubric = task.get("rubric", {})
    expected_terms = ", ".join(rubric.get("expected_terms", [])) or "none"
    forbidden_terms = ", ".join(rubric.get("forbidden_terms", [])) or "none"
    banned_phrases = ", ".join(rubric.get("banned_phrases", [])) or "none"
    judge_dimensions = ", ".join(task.get("scoring_config", {}).get("judge_dimensions", [])) or "none"
    return (
        f"Write a {task.get('channel')} {task.get('message_kind')} for "
        f"{prospect.get('contact_role', 'the prospect')} at {prospect.get('company_name', 'the company')} "
        f"({prospect.get('company_stage', 'unknown stage')}).\n"
        f"Failure dimension focus: {task.get('failure_dimension')}.\n"
        f"Judge dimensions: {judge_dimensions}.\n"
        f"Prior thread summary: {prior_thread.get('summary', '') or 'none'}\n"
        f"Signals:\n{render_signal_summary(task)}\n"
        f"Expected behavior: {task.get('ground_truth', {}).get('expected_behavior', '')}\n"
        f"Required terms: {expected_terms}\n"
        f"Forbidden terms: {forbidden_terms}\n"
        f"Banned phrases: {banned_phrases}\n"
        "Keep the response grounded, professional, and limited to one buyer-facing next step."
    )


def fallback_subject(task: dict[str, Any]) -> str:
    return f"Question on {task.get('failure_dimension', 'workflow').replace('_', ' ')}"


def build_rejected_candidate(task: dict[str, Any]) -> tuple[dict[str, str], str]:
    channel = task.get("channel")
    name = task.get("input", {}).get("prospect", {}).get("contact_role", "there")
    source_mode = task.get("source_mode")
    failure_dimension = task.get("failure_dimension")
    body: str
    rejected_source = "controlled_rubric_variant"

    if failure_dimension == "gap_condescension":
        body = (
            "Hi there, you are behind the curve and need to fix this basic AI gap fast. "
            "Let's book a quick chat so I can explain what your team should already be doing."
        )
    elif failure_dimension == "ai_maturity_consistency":
        body = (
            "Hi there, your AI maturity is low and you just need to automate more. "
            "Book time with me and I will tell you the right workflow."
        )
    elif failure_dimension == "signal_grounding":
        body = (
            "Hi there, it is obvious from the public signal that your workflow is broken and your team is falling behind. "
            "Can you confirm who owns the issue?"
        )
    elif failure_dimension == "style_guide_adherence":
        body = (
            "Hi there, I hope this email finds you well. Your world-class team looks production-ready, "
            "so let's do a quick chat about the live run."
        )
        rejected_source = "style_guide_bad_example"
    elif failure_dimension == "next_step_quality":
        body = (
            "Hi there, this looks interesting. Can you send one example and schedule a call next week so we can also review pricing?"
        )
    else:
        body = "Hi there, quick question. N/A."

    if source_mode == "trace_derived":
        rejected_source = "week10_trace_inspired_variant"

    if channel == "email":
        subject = "Quick chat about your gap"
        if failure_dimension == "output_validity":
            subject = "Quick question"
        return {"subject": subject, "body": body}, rejected_source
    return {"body": body}, rejected_source


def build_preference_seed(task: dict[str, Any]) -> dict[str, Any]:
    rejected_candidate, rejected_source = build_rejected_candidate(task)
    return {
        "id": f"orpo-{task['task_id']}",
        "source_task_id": task["task_id"],
        "source_partition": task["partition"],
        "failure_dimension": task["failure_dimension"],
        "prompt": render_prompt(task),
        "chosen": format_candidate_output(task["candidate_output"]),
        "rejected": format_candidate_output(rejected_candidate),
        "chosen_source": "benchmark_candidate_output",
        "rejected_source": rejected_source,
        "rejected_model": LOCAL_REJECTED_MODEL,
        "metadata": {
            "source_mode": task.get("source_mode"),
            "difficulty": task.get("difficulty"),
            "channel": task.get("channel"),
            "message_kind": task.get("message_kind"),
            "probe_id": task.get("metadata", {}).get("probe_id"),
            "source_artifact": task.get("metadata", {}).get("source_artifact"),
            "style_guide_version": task.get("metadata", {}).get("style_guide_version"),
            "judge_dimensions": task.get("scoring_config", {}).get("judge_dimensions", []),
            "deterministic_dimensions": task.get("scoring_config", {}).get(
                "deterministic_dimensions", []
            ),
            "rejected_variant_policy": "local_rule_based_controlled_variant",
            "historical_rejected_output_imported": False,
        },
    }


def validate_seed_record(row: dict[str, Any]) -> None:
    missing = [field for field in ROW_REQUIRED_FIELDS if field not in row]
    if missing:
        raise ValueError(f"Preference seed {row.get('id', '<unknown>')} missing fields: {missing}")
    for field in ("prompt", "chosen", "rejected", "source_task_id", "source_partition"):
        value = row.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Preference seed {row.get('id', '<unknown>')} has empty required string field {field}."
            )
    if row["chosen"] == row["rejected"]:
        raise ValueError(f"Preference seed {row['id']} has identical chosen and rejected outputs.")
    if row["source_partition"] == "held_out":
        raise ValueError(f"Preference seed {row['id']} uses held_out, which is forbidden.")


def build_summary(
    *,
    output_path: Path,
    tasks: list[dict[str, Any]],
    prepared_rows: list[dict[str, Any]],
    dropped_rows: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "output_path": str(output_path),
        "task_count": len(tasks),
        "pair_count": len(prepared_rows),
        "source_partition_counts": Counter(row["source_partition"] for row in prepared_rows),
        "failure_dimension_counts": Counter(row["failure_dimension"] for row in prepared_rows),
        "rejected_source_counts": Counter(row["rejected_source"] for row in prepared_rows),
        "held_out_exclusion_passed": all(row["source_partition"] != "held_out" for row in prepared_rows),
        "skipped_count": len(dropped_rows),
        "skipped_examples": dropped_rows[:10],
    }


def main() -> int:
    args = parse_args()
    tasks = load_public_tasks(args.dataset_root)
    task_index = {task["task_id"]: task["partition"] for task in tasks}
    seeds = [build_preference_seed(task) for task in tasks]
    for seed in seeds:
        validate_seed_record(seed)
    prepared_rows, dropped_rows = prepare_records(
        seeds,
        task_index=task_index,
        chosen_rewrite_model=args.chosen_rewrite_model,
        chosen_rewrite_judge_model=args.judge_model,
        default_rejected_model=LOCAL_REJECTED_MODEL,
    )
    summary = build_summary(
        output_path=args.output,
        tasks=tasks,
        prepared_rows=prepared_rows,
        dropped_rows=dropped_rows,
    )
    print(json.dumps(summary, indent=2, default=str))

    if args.dry_run:
        return 0
    if dropped_rows:
        return 1
    write_jsonl(args.output, prepared_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
