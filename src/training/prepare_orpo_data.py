"""Prepare ORPO preference data with explicit provenance and rotation checks."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import REPO_ROOT, read_jsonl, write_jsonl
from src.generation.synthesis_policy import (
    DEFAULT_GENERATION_MODEL,
    DEFAULT_JUDGE_MODEL,
    enforce_rotation,
)

PREFERENCE_REQUIRED_FIELDS = ("id", "prompt", "chosen", "rejected")
SOURCE_PARTITIONS = ("train", "dev", "held_out")
INDEXED_SOURCE_PARTITIONS = ("train", "dev")
OUTPUT_PARTITION = "train"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare ORPO preference pairs and enforce chosen-rewrite judge rotation."
    )
    parser.add_argument("--input", type=Path, required=True, help="Input JSONL preference seed file.")
    parser.add_argument("--output", type=Path, required=True, help="Output JSONL prepared preference file.")
    parser.add_argument(
        "--dataset-root",
        type=Path,
        default=REPO_ROOT / "tenacious_bench_v0.1",
        help="Dataset root used to validate source_task_id and source_partition metadata.",
    )
    parser.add_argument(
        "--chosen-rewrite-model",
        default=DEFAULT_GENERATION_MODEL,
        help="Model family that authored the chosen rewrite.",
    )
    parser.add_argument(
        "--judge-model",
        default=DEFAULT_JUDGE_MODEL,
        help="Model family that judged the chosen rewrite for acceptance.",
    )
    parser.add_argument(
        "--rejected-model",
        default=None,
        help="Fallback model family that authored the rejected sample when not stored per record.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and summarize preference data without writing the prepared output.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when any rows are dropped instead of treating drops as a partial-success summary.",
    )
    return parser.parse_args()


def index_dataset_tasks(dataset_root: Path) -> dict[str, str]:
    task_index: dict[str, str] = {}
    # Keep held_out completely outside preference-prep reads. We still reject any
    # claimed held_out source_partition explicitly during record validation.
    for partition in INDEXED_SOURCE_PARTITIONS:
        partition_dir = dataset_root / partition
        if not partition_dir.exists():
            continue
        for path in sorted(partition_dir.glob("*.jsonl")):
            for row in read_jsonl(path):
                task_id = row.get("task_id")
                if task_id:
                    task_index[str(task_id)] = partition
    return task_index


def validate_preference_pair_rotation(
    rejected_model: str,
    chosen_rewrite_model: str,
    chosen_rewrite_judge_model: str,
) -> None:
    enforce_rotation(chosen_rewrite_model, chosen_rewrite_judge_model)
    enforce_rotation(rejected_model, chosen_rewrite_judge_model)


def source_task_fields(record: dict[str, Any]) -> tuple[str | None, str | None]:
    metadata = record.get("metadata", {}) if isinstance(record.get("metadata", {}), dict) else {}
    source_task_id = record.get("source_task_id") or metadata.get("source_task_id")
    source_partition = record.get("source_partition") or metadata.get("source_partition")
    return None if source_task_id is None else str(source_task_id), source_partition


def validate_source_task(
    source_task_id: str | None,
    source_partition: str | None,
    task_index: dict[str, str],
    record_id: str,
) -> tuple[str, str]:
    if not source_task_id:
        raise ValueError(
            f"Preference record {record_id} is missing source_task_id, so R3 provenance cannot be checked."
        )
    if source_partition not in SOURCE_PARTITIONS:
        raise ValueError(
            f"Preference record {record_id} has invalid source_partition={source_partition!r}."
        )
    if source_partition == "held_out":
        raise ValueError(
            f"Preference record {record_id} cites held_out source_task_id={source_task_id}, which is forbidden."
        )
    actual_partition = task_index.get(source_task_id)
    if actual_partition is None:
        raise ValueError(
            f"Preference record {record_id} cites unknown source_task_id={source_task_id}."
        )
    if actual_partition != source_partition:
        raise ValueError(
            f"Preference record {record_id} claims source_partition={source_partition} for "
            f"source_task_id={source_task_id}, but dataset root has it in {actual_partition}."
        )
    return source_task_id, source_partition


def prepare_preference_record(
    record: dict[str, Any],
    *,
    task_index: dict[str, str],
    chosen_rewrite_model: str,
    chosen_rewrite_judge_model: str,
    default_rejected_model: str | None = None,
) -> dict[str, Any]:
    missing = [field for field in PREFERENCE_REQUIRED_FIELDS if not record.get(field)]
    if missing:
        raise ValueError(f"Preference record missing required field(s): {', '.join(missing)}")
    for field in ("prompt", "chosen", "rejected"):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Preference record {record.get('id', '<unknown>')} has empty required text field {field}."
            )
    if record.get("chosen") == record.get("rejected"):
        raise ValueError(
            f"Preference record {record.get('id', '<unknown>')} has identical chosen and rejected outputs."
        )

    prepared = deepcopy(record)
    metadata = prepared.setdefault("metadata", {})
    if not isinstance(metadata, dict):
        raise ValueError(
            f"Preference record {prepared.get('id', '<unknown>')} has non-object metadata."
        )
    record_id = str(prepared.get("id", "<unknown>"))
    rejected_model = (
        metadata.get("rejected_model")
        or prepared.get("rejected_model")
        or default_rejected_model
    )
    if not rejected_model:
        raise ValueError(
            f"Preference record {record_id} is missing rejected_model, "
            "so R2 rotation cannot be enforced."
        )

    source_task_id, source_partition = source_task_fields(prepared)
    source_task_id, source_partition = validate_source_task(
        source_task_id,
        source_partition,
        task_index,
        record_id,
    )
    validate_preference_pair_rotation(
        str(rejected_model),
        chosen_rewrite_model,
        chosen_rewrite_judge_model,
    )
    prepared["output_partition"] = OUTPUT_PARTITION
    prepared["source_task_id"] = source_task_id
    prepared["source_partition"] = source_partition
    metadata["rejected_model"] = str(rejected_model)
    metadata["chosen_rewrite_model"] = chosen_rewrite_model
    metadata["chosen_rewrite_judge_model"] = chosen_rewrite_judge_model
    metadata["source_task_id"] = source_task_id
    metadata["source_partition"] = source_partition
    return prepared


def prepare_records(
    rows: list[dict[str, Any]],
    *,
    task_index: dict[str, str],
    chosen_rewrite_model: str,
    chosen_rewrite_judge_model: str,
    default_rejected_model: str | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    prepared_rows: list[dict[str, Any]] = []
    dropped_rows: list[dict[str, str]] = []
    for row in rows:
        try:
            prepared_rows.append(
                prepare_preference_record(
                    row,
                    task_index=task_index,
                    chosen_rewrite_model=chosen_rewrite_model,
                    chosen_rewrite_judge_model=chosen_rewrite_judge_model,
                    default_rejected_model=default_rejected_model,
                )
            )
        except ValueError as exc:
            dropped_rows.append(
                {
                    "id": str(row.get("id", "<unknown>")),
                    "reason": str(exc),
                }
            )
    return prepared_rows, dropped_rows


def build_summary(
    *,
    input_path: Path,
    output_path: Path,
    dataset_root: Path,
    input_count: int,
    prepared_count: int,
    dropped_rows: list[dict[str, str]],
    chosen_rewrite_model: str,
    chosen_rewrite_judge_model: str,
    dry_run: bool,
    strict: bool,
) -> dict[str, Any]:
    return {
        "input_path": str(input_path),
        "output_path": str(output_path),
        "dataset_root": str(dataset_root),
        "input_count": input_count,
        "prepared_count": prepared_count,
        "dropped_count": len(dropped_rows),
        "dry_run": dry_run,
        "strict": strict,
        "output_partition": OUTPUT_PARTITION,
        "chosen_rewrite_model": chosen_rewrite_model,
        "chosen_rewrite_judge_model": chosen_rewrite_judge_model,
        "dropped_examples": dropped_rows[:10],
    }


def main() -> int:
    args = parse_args()
    rows = read_jsonl(args.input)
    task_index = index_dataset_tasks(args.dataset_root)
    prepared_rows, dropped_rows = prepare_records(
        rows,
        task_index=task_index,
        chosen_rewrite_model=args.chosen_rewrite_model,
        chosen_rewrite_judge_model=args.judge_model,
        default_rejected_model=args.rejected_model,
    )
    summary = build_summary(
        input_path=args.input,
        output_path=args.output,
        dataset_root=args.dataset_root,
        input_count=len(rows),
        prepared_count=len(prepared_rows),
        dropped_rows=dropped_rows,
        chosen_rewrite_model=args.chosen_rewrite_model,
        chosen_rewrite_judge_model=args.judge_model,
        dry_run=args.dry_run,
        strict=args.strict,
    )
    print(json.dumps(summary, indent=2))

    if args.dry_run:
        return 0
    if prepared_rows:
        write_jsonl(args.output, prepared_rows)
    if args.strict and dropped_rows:
        return 1
    if not prepared_rows:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
