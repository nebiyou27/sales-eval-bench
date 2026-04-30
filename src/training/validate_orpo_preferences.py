"""Validate prepared ORPO preference pairs and summarize coverage."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import REPO_ROOT, read_jsonl
from src.training.prepare_orpo_data import index_dataset_tasks, validate_source_task


DEFAULT_INPUT = REPO_ROOT / "training_data" / "orpo_preferences.jsonl"
DEFAULT_DATASET_ROOT = REPO_ROOT / "tenacious_bench_v0.1"
REQUIRED_FIELDS = (
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
    parser = argparse.ArgumentParser(description="Validate ORPO preference pairs.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--dataset-root", type=Path, default=DEFAULT_DATASET_ROOT)
    return parser.parse_args()


def validate_row(row: dict[str, Any], task_index: dict[str, str]) -> list[str]:
    errors: list[str] = []
    row_id = str(row.get("id", "<unknown>"))
    for field in REQUIRED_FIELDS:
        if field not in row:
            errors.append(f"{row_id}: missing field {field}")
    for field in ("prompt", "chosen", "rejected", "source_task_id", "source_partition"):
        value = row.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{row_id}: empty required string field {field}")
    if isinstance(row.get("chosen"), str) and isinstance(row.get("rejected"), str):
        if row["chosen"] == row["rejected"]:
            errors.append(f"{row_id}: chosen and rejected are identical")
    if row.get("source_partition") == "held_out":
        errors.append(f"{row_id}: held_out source_partition is forbidden")
    if "held_out" in str(row.get("source_task_id", "")):
        errors.append(f"{row_id}: held_out-like source_task_id is forbidden")
    try:
        validate_source_task(
            str(row.get("source_task_id")) if row.get("source_task_id") is not None else None,
            row.get("source_partition"),
            task_index,
            row_id,
        )
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def build_summary(rows: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "source_partition_counts": Counter(row.get("source_partition") for row in rows),
        "failure_dimension_counts": Counter(row.get("failure_dimension") for row in rows),
        "rejected_source_counts": Counter(row.get("rejected_source") for row in rows),
        "held_out_exclusion_passed": not any(
            row.get("source_partition") == "held_out" or "held_out" in str(row.get("source_task_id", ""))
            for row in rows
        ),
        "error_count": len(errors),
        "errors": errors[:20],
    }


def main() -> int:
    args = parse_args()
    rows = read_jsonl(args.input)
    task_index = index_dataset_tasks(args.dataset_root)
    errors: list[str] = []
    for row in rows:
        errors.extend(validate_row(row, task_index))
    summary = build_summary(rows, errors)
    print(json.dumps(summary, indent=2, default=str))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
