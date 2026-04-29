"""Inspect pairwise embedding cosine scores across current benchmark tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import REPO_ROOT
from src.generation.contamination_check import (
    DEFAULT_EMBEDDING_MODEL,
    cosine_similarity,
    embedding_vectors_for_rows,
    partition_rows,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calibrate embedding cosine thresholds against the current dataset."
    )
    parser.add_argument(
        "--dataset-root",
        type=Path,
        default=REPO_ROOT / "tenacious_bench_v0.1",
        help="Root folder containing train/dev/held_out partitions.",
    )
    parser.add_argument(
        "--embedding-model",
        default=DEFAULT_EMBEDDING_MODEL,
        help="Local embedding model name or path.",
    )
    return parser.parse_args()


def summarize_scores(scores: list[float]) -> dict[str, float | int | None]:
    if not scores:
        return {"count": 0, "min": None, "median": None, "mean": None, "max": None}
    ordered = sorted(scores)
    return {
        "count": len(ordered),
        "min": round(ordered[0], 3),
        "median": round(statistics.median(ordered), 3),
        "mean": round(statistics.fmean(ordered), 3),
        "max": round(ordered[-1], 3),
    }


def main() -> int:
    args = parse_args()
    rows = []
    for partition in ("train", "dev", "held_out"):
        rows.extend(partition_rows(args.dataset_root, partition))
    embeddings, status = embedding_vectors_for_rows(rows, args.embedding_model)
    if embeddings is None:
        print(
            json.dumps(
                {
                    "dataset_root": str(args.dataset_root),
                    "embedding_model": args.embedding_model,
                    "embedding_check_status": status,
                },
                indent=2,
            )
        )
        return 1

    same_probe_scores: list[float] = []
    different_probe_scores: list[float] = []
    pair_rows: list[dict[str, Any]] = []
    for left_index, left_row in enumerate(rows):
        left_id = left_row.get("task_id", "")
        left_probe = left_row.get("metadata", {}).get("probe_id", "")
        left_partition = left_row.get("partition", "")
        for right_row in rows[left_index + 1 :]:
            right_id = right_row.get("task_id", "")
            right_probe = right_row.get("metadata", {}).get("probe_id", "")
            right_partition = right_row.get("partition", "")
            cosine = cosine_similarity(embeddings[left_id], embeddings[right_id])
            target = same_probe_scores if left_probe and left_probe == right_probe else different_probe_scores
            target.append(cosine)
            pair_rows.append(
                {
                    "left_task_id": left_id,
                    "left_probe_id": left_probe,
                    "left_partition": left_partition,
                    "right_task_id": right_id,
                    "right_probe_id": right_probe,
                    "right_partition": right_partition,
                    "same_probe": bool(left_probe and left_probe == right_probe),
                    "embedding_cosine": round(cosine, 3),
                }
            )

    top_pairs = sorted(pair_rows, key=lambda row: row["embedding_cosine"], reverse=True)[:10]
    print(
        json.dumps(
            {
                "dataset_root": str(args.dataset_root),
                "embedding_model": args.embedding_model,
                "embedding_check_status": status,
                "task_count": len(rows),
                "same_probe_summary": summarize_scores(same_probe_scores),
                "different_probe_summary": summarize_scores(different_probe_scores),
                "top_pairs": top_pairs,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
