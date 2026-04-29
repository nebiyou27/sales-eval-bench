"""Shared helpers for Tenacious-Bench dataset authoring scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schema.json"


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validator() -> Draft202012Validator:
    return Draft202012Validator(load_schema())


def validate_task(task: dict[str, Any]) -> None:
    errors = sorted(validator().iter_errors(task), key=lambda err: err.path)
    if errors:
        rendered = "; ".join(error.message for error in errors)
        raise ValueError(f"Task {task.get('task_id', '<unknown>')} failed schema validation: {rendered}")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(row, ensure_ascii=True) for row in rows]
    payload = "\n".join(lines)
    if lines:
        payload += "\n"
    path.write_text(payload, encoding="utf-8")


def prompt_manifest_path(output_path: Path) -> Path:
    return output_path.with_name(output_path.stem + "_prompt_manifest.jsonl")


HELD_OUT_TRACES_PATH = REPO_ROOT / "seed" / "held_out_traces.jsonl"


def load_held_out_trace_ids(path: Path = HELD_OUT_TRACES_PATH) -> set[str]:
    return {row["simulation_id"] for row in read_jsonl(path) if "simulation_id" in row}


def assert_no_held_out_leakage(
    task: dict[str, Any],
    partition: str,
    held_out_ids: set[str],
) -> None:
    if partition == "held_out":
        return
    cited = set(task.get("metadata", {}).get("source_trace_ids", []) or [])
    leaked = cited & held_out_ids
    if leaked:
        raise ValueError(
            f"Task {task.get('task_id', '<unknown>')} in partition '{partition}' "
            f"cites held-out trace(s): {sorted(leaked)}"
        )
