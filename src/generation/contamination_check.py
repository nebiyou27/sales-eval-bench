"""Scaffold contamination checks for Tenacious-Bench partitions.

Current checks:
- 8-gram overlap between held-out tasks and train/dev tasks
- time-shift provenance presence for synthetic signal-grounding tasks
- lexical cosine proxy for near-duplicate detection (placeholder until the
  embedding model is added to the toolchain)
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import REPO_ROOT, load_held_out_trace_ids, read_jsonl, validate_task


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run contamination checks across benchmark partitions.")
    parser.add_argument(
        "--dataset-root",
        type=Path,
        default=REPO_ROOT / "tenacious_bench_v0.1",
        help="Root folder containing train/dev/held_out partitions.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "src" / "generation" / "contamination_check.json",
        help="Where to write the contamination report.",
    )
    return parser.parse_args()


def partition_rows(dataset_root: Path, partition: str) -> list[dict[str, Any]]:
    partition_dir = dataset_root / partition
    rows: list[dict[str, Any]] = []
    if not partition_dir.exists():
        return rows
    for path in sorted(partition_dir.glob("*.jsonl")):
        for row in read_jsonl(path):
            try:
                validate_task(row)
            except ValueError:
                continue
            rows.append(row)
    return rows


def normalized_text(task: dict[str, Any]) -> str:
    prospect = task.get("input", {}).get("prospect", {})
    signals = task.get("input", {}).get("hiring_signal_brief", {}).get("signals", [])
    signal_evidence = " ".join(signal.get("evidence", "") for signal in signals if isinstance(signal, dict))
    subject = task.get("candidate_output", {}).get("subject", "")
    body = task.get("candidate_output", {}).get("body", "")
    fields = [
        task.get("task_id", ""),
        prospect.get("company_name", ""),
        prospect.get("contact_role", ""),
        signal_evidence,
        subject,
        body,
    ]
    text = " ".join(field for field in fields if isinstance(field, str))
    return re.sub(r"\s+", " ", text.lower()).strip()


def ngrams(text: str, n: int = 8) -> set[tuple[str, ...]]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    if len(tokens) < n:
        return set()
    return {tuple(tokens[index : index + n]) for index in range(len(tokens) - n + 1)}


def lexical_cosine(left: str, right: str) -> float:
    left_counts = Counter(re.findall(r"[a-z0-9]+", left.lower()))
    right_counts = Counter(re.findall(r"[a-z0-9]+", right.lower()))
    if not left_counts or not right_counts:
        return 0.0
    overlap = set(left_counts) & set(right_counts)
    numerator = sum(left_counts[token] * right_counts[token] for token in overlap)
    left_norm = math.sqrt(sum(value * value for value in left_counts.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counts.values()))
    return numerator / (left_norm * right_norm)


def compare_partitions(held_out_rows: list[dict[str, Any]], other_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    other_payload = [
        (row.get("task_id", ""), normalized_text(row), ngrams(normalized_text(row)))
        for row in other_rows
    ]
    for held_out in held_out_rows:
        held_id = held_out.get("task_id", "")
        held_text = normalized_text(held_out)
        held_ngrams = ngrams(held_text)
        for other_id, other_text, other_ngrams in other_payload:
            shared_ngrams = held_ngrams & other_ngrams
            lexical_score = lexical_cosine(held_text, other_text)
            if shared_ngrams or lexical_score >= 0.85:
                findings.append(
                    {
                        "held_out_task_id": held_id,
                        "other_task_id": other_id,
                        "shared_8grams": len(shared_ngrams),
                        "lexical_cosine_proxy": round(lexical_score, 3),
                    }
                )
    return findings


def time_shift_findings(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for row in rows:
        if row.get("source_mode") == "synthetic" and row.get("failure_dimension") == "signal_grounding":
            provenance = row.get("metadata", {}).get("retrieval_provenance")
            if not provenance:
                findings.append(
                    {
                        "task_id": row.get("task_id", ""),
                        "reason": "synthetic signal-grounding task missing retrieval_provenance",
                    }
                )
    return findings


def source_trace_findings(
    train_rows: list[dict[str, Any]],
    dev_rows: list[dict[str, Any]],
    held_out_rows: list[dict[str, Any]],
    seed_held_out_ids: set[str],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    def cited(task: dict[str, Any]) -> set[str]:
        return set(task.get("metadata", {}).get("source_trace_ids", []) or [])

    for partition_name, rows in (("train", train_rows), ("dev", dev_rows)):
        for row in rows:
            leaked = cited(row) & seed_held_out_ids
            if leaked:
                findings.append(
                    {
                        "task_id": row.get("task_id", ""),
                        "partition": partition_name,
                        "reason": "cites a seed held-out trace id",
                        "leaked_trace_ids": sorted(leaked),
                    }
                )

    held_out_cited = {tid for row in held_out_rows for tid in cited(row)}
    for partition_name, rows in (("train", train_rows), ("dev", dev_rows)):
        for row in rows:
            overlap = cited(row) & held_out_cited
            if overlap:
                findings.append(
                    {
                        "task_id": row.get("task_id", ""),
                        "partition": partition_name,
                        "reason": "shares source_trace_ids with a held-out task",
                        "leaked_trace_ids": sorted(overlap),
                    }
                )
    return findings


def build_report(dataset_root: Path) -> dict[str, Any]:
    train_rows = partition_rows(dataset_root, "train")
    dev_rows = partition_rows(dataset_root, "dev")
    held_out_rows = partition_rows(dataset_root, "held_out")
    overlap_findings = compare_partitions(held_out_rows, train_rows + dev_rows)
    provenance_findings = time_shift_findings(train_rows + dev_rows + held_out_rows)
    seed_held_out_ids = load_held_out_trace_ids()
    trace_findings = source_trace_findings(train_rows, dev_rows, held_out_rows, seed_held_out_ids)
    held_out_status = "pending_no_held_out_data" if not held_out_rows else "checked"
    structural_clean = not trace_findings
    if not held_out_rows:
        contamination_pass = None if structural_clean else False
    else:
        contamination_pass = structural_clean and not overlap_findings and not provenance_findings
    report = {
        "dataset_root": str(dataset_root),
        "partition_counts": {
            "train": len(train_rows),
            "dev": len(dev_rows),
            "held_out": len(held_out_rows),
        },
        "held_out_status": held_out_status,
        "seed_held_out_trace_count": len(seed_held_out_ids),
        "n_gram_threshold": 8,
        "lexical_cosine_proxy_threshold": 0.85,
        "embedding_check_status": "proxy_only_pending_embedding_model",
        "overlap_findings": overlap_findings,
        "time_shift_findings": provenance_findings,
        "source_trace_findings": trace_findings,
        "pass": contamination_pass,
    }
    return report


def main() -> int:
    args = parse_args()
    report = build_report(args.dataset_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["pass"] is None:
        return 0
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
