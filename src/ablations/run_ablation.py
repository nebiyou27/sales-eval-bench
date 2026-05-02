"""Shared ablation harness for Tenacious-Bench comparisons.

The harness supports:
- Delta A: trained component vs Week 10 baseline on held-out
- Delta B: trained component vs prompt-only version of the same backbone
- Delta C: informational tau2 reference comparison without re-running tau2
- Cost-Pareto summaries with timing/token/cost aggregation
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
import statistics
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import REPO_ROOT, read_jsonl
from src.scoring.scoring_evaluator import score_candidate


DEFAULT_HELD_OUT_DIR = REPO_ROOT / "tenacious_bench_v0.1" / "held_out"


@dataclass(frozen=True)
class TaskOutcome:
    task_id: str
    passed: bool
    total: float
    latency_ms: float
    input_tokens: int
    output_tokens: int
    usd_cost: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Tenacious-Bench ablation comparisons.")
    parser.add_argument(
        "--comparison",
        choices=("delta_a", "delta_b", "delta_c", "cost_pareto", "all"),
        default="all",
        help="Which comparison to run from the shared harness.",
    )
    parser.add_argument(
        "--held-out-dir",
        type=Path,
        default=DEFAULT_HELD_OUT_DIR,
        help="Directory containing held-out task JSONL files.",
    )
    parser.add_argument("--baseline-predictions", type=Path, help="Week 10 baseline prediction JSONL.")
    parser.add_argument("--trained-predictions", type=Path, help="Trained-component prediction JSONL.")
    parser.add_argument("--prompt-only-predictions", type=Path, help="Prompt-only prediction JSONL.")
    parser.add_argument(
        "--tau2-reference",
        type=Path,
        help="Informational JSON file with tau2 reference metrics. This is never re-run by the harness.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "docs" / "ablation_summary.json",
        help="Where to write the ablation summary.",
    )
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=11)
    return parser.parse_args()


def load_tasks(held_out_dir: Path) -> dict[str, dict[str, Any]]:
    tasks: dict[str, dict[str, Any]] = {}
    for path in sorted(held_out_dir.glob("*.jsonl")):
        for row in read_jsonl(path):
            task_id = row.get("task_id")
            if task_id:
                tasks[str(task_id)] = row
    return tasks


def load_predictions(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    rows = read_jsonl(path)
    return {str(row.get("task_id", "")): row for row in rows if row.get("task_id")}


def outcome_for_task(task: dict[str, Any], prediction: dict[str, Any]) -> TaskOutcome:
    if "scores" in prediction and "passed" in prediction and "total" in prediction:
        passed = bool(prediction["passed"])
        total = float(prediction["total"])
    else:
        candidate = prediction.get("candidate_output", task.get("candidate_output", {}))
        scored = score_candidate(task, candidate)
        passed = scored.passed
        total = scored.total
    return TaskOutcome(
        task_id=str(task.get("task_id", "")),
        passed=passed,
        total=total,
        latency_ms=float(prediction.get("latency_ms", 0.0) or 0.0),
        input_tokens=int(prediction.get("input_tokens", 0) or 0),
        output_tokens=int(prediction.get("output_tokens", 0) or 0),
        usd_cost=float(prediction.get("usd_cost", 0.0) or 0.0),
    )


def build_outcomes(
    tasks: dict[str, dict[str, Any]],
    predictions: dict[str, dict[str, Any]],
) -> tuple[list[TaskOutcome], list[str]]:
    outcomes: list[TaskOutcome] = []
    failures: list[str] = []
    for task_id, task in tasks.items():
        prediction = predictions.get(task_id)
        if prediction is None:
            failures.append(f"missing_prediction:{task_id}")
            continue
        try:
            outcomes.append(outcome_for_task(task, prediction))
        except Exception as exc:
            failures.append(f"failed_to_score:{task_id}:{type(exc).__name__}")
    return outcomes, failures


def paired_deltas(left: list[TaskOutcome], right: list[TaskOutcome], attr: str) -> list[float]:
    right_index = {row.task_id: row for row in right}
    deltas: list[float] = []
    for left_row in left:
        other = right_index.get(left_row.task_id)
        if other is None:
            continue
        deltas.append(float(getattr(left_row, attr)) - float(getattr(other, attr)))
    return deltas


def paired_bootstrap_ci(
    deltas: list[float],
    *,
    samples: int,
    seed: int,
) -> dict[str, float | None]:
    if not deltas:
        return {"mean_delta": None, "ci_low": None, "ci_high": None}
    rng = random.Random(seed)
    means: list[float] = []
    for _ in range(samples):
        draw = [deltas[rng.randrange(len(deltas))] for _ in range(len(deltas))]
        means.append(sum(draw) / len(draw))
    means.sort()
    low_index = int(0.025 * (samples - 1))
    high_index = int(0.975 * (samples - 1))
    return {
        "mean_delta": round(sum(deltas) / len(deltas), 4),
        "ci_low": round(means[low_index], 4),
        "ci_high": round(means[high_index], 4),
    }


def paired_sign_flip_p_value(
    deltas: list[float],
    *,
    samples: int,
    seed: int,
) -> float | None:
    if not deltas:
        return None
    observed = abs(sum(deltas) / len(deltas))
    rng = random.Random(seed)
    extreme = 0
    for _ in range(samples):
        flipped = [delta if rng.random() < 0.5 else -delta for delta in deltas]
        simulated = abs(sum(flipped) / len(flipped))
        if simulated >= observed:
            extreme += 1
    return round((extreme + 1) / (samples + 1), 4)


def pass_rate(outcomes: list[TaskOutcome]) -> float | None:
    if not outcomes:
        return None
    return round(sum(1 for row in outcomes if row.passed) / len(outcomes), 4)


def cost_summary(outcomes: list[TaskOutcome]) -> dict[str, float | int | None]:
    if not outcomes:
        return {
            "task_count": 0,
            "avg_latency_ms": None,
            "avg_input_tokens": None,
            "avg_output_tokens": None,
            "avg_usd_cost": None,
            "total_usd_cost": None,
        }
    return {
        "task_count": len(outcomes),
        "avg_latency_ms": round(statistics.fmean(row.latency_ms for row in outcomes), 3),
        "avg_input_tokens": round(statistics.fmean(row.input_tokens for row in outcomes), 3),
        "avg_output_tokens": round(statistics.fmean(row.output_tokens for row in outcomes), 3),
        "avg_usd_cost": round(statistics.fmean(row.usd_cost for row in outcomes), 6),
        "total_usd_cost": round(sum(row.usd_cost for row in outcomes), 6),
    }


def delta_report(
    label: str,
    improved: list[TaskOutcome],
    baseline: list[TaskOutcome],
    *,
    bootstrap_samples: int,
    seed: int,
) -> dict[str, Any]:
    pass_deltas = paired_deltas(improved, baseline, "passed")
    score_deltas = paired_deltas(improved, baseline, "total")
    return {
        "comparison": label,
        "improved_pass_rate": pass_rate(improved),
        "baseline_pass_rate": pass_rate(baseline),
        "pass_rate_lift": None
        if pass_rate(improved) is None or pass_rate(baseline) is None
        else round(pass_rate(improved) - pass_rate(baseline), 4),
        "paired_bootstrap_pass_rate": paired_bootstrap_ci(
            pass_deltas,
            samples=bootstrap_samples,
            seed=seed,
        ),
        "paired_bootstrap_score": paired_bootstrap_ci(
            score_deltas,
            samples=bootstrap_samples,
            seed=seed + 1,
        ),
        "p_value_sign_flip_score": paired_sign_flip_p_value(
            score_deltas,
            samples=bootstrap_samples,
            seed=seed + 2,
        ),
    }


def informational_tau2_report(reference_path: Path | None) -> dict[str, Any]:
    if reference_path is None or not reference_path.exists():
        return {
            "status": "missing_reference",
            "note": "Delta C is informational only and does not re-run tau2.",
        }
    payload = json.loads(reference_path.read_text(encoding="utf-8"))
    return {
        "status": "loaded_reference",
        "note": "Delta C is informational only and does not re-run tau2.",
        "reference": payload,
    }


def main() -> int:
    args = parse_args()
    tasks = load_tasks(args.held_out_dir)
    summary: dict[str, Any] = {
        "comparison": args.comparison,
        "held_out_task_count": len(tasks),
        "failures": [],
    }

    baseline_predictions = load_predictions(args.baseline_predictions)
    trained_predictions = load_predictions(args.trained_predictions)
    prompt_only_predictions = load_predictions(args.prompt_only_predictions)

    baseline_outcomes, baseline_failures = build_outcomes(tasks, baseline_predictions)
    trained_outcomes, trained_failures = build_outcomes(tasks, trained_predictions)
    prompt_only_outcomes, prompt_only_failures = build_outcomes(tasks, prompt_only_predictions)
    summary["failures"].extend(baseline_failures + trained_failures + prompt_only_failures)

    if args.comparison in {"delta_a", "all"}:
        summary["delta_a"] = delta_report(
            "trained_vs_week10_baseline",
            trained_outcomes,
            baseline_outcomes,
            bootstrap_samples=args.bootstrap_samples,
            seed=args.seed,
        )

    if args.comparison in {"delta_b", "all"}:
        summary["delta_b"] = delta_report(
            "trained_vs_prompt_only_same_backbone",
            trained_outcomes,
            prompt_only_outcomes,
            bootstrap_samples=args.bootstrap_samples,
            seed=args.seed + 10,
        )

    if args.comparison in {"delta_c", "all"}:
        summary["delta_c"] = informational_tau2_report(args.tau2_reference)

    if args.comparison in {"cost_pareto", "all"}:
        summary["cost_pareto"] = {
            "baseline": cost_summary(baseline_outcomes),
            "trained": cost_summary(trained_outcomes),
            "prompt_only": cost_summary(prompt_only_outcomes),
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
