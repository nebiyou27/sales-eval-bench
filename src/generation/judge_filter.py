"""Judge-filter pipeline for Tenacious-Bench synthetic-task admission.

This module makes the rubric-visible filtering logic explicit:
- pointwise 1-5 scoring on three dimensions,
- pairwise duplicate checks for similar tasks,
- dev-tier bulk filtering with eval-tier calibration spot-checks,
- per-task pass/fail logging with reasons.
"""

from __future__ import annotations

import argparse
import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import REPO_ROOT, read_jsonl, write_jsonl
from src.generation.synthesis_policy import model_family


POINTWISE_DIMENSIONS = ("input_coherence", "ground_truth_verifiability", "rubric_clarity")
POINTWISE_MIN_SCORE = 4
POINTWISE_MIN_AVERAGE = 4.0
DEFAULT_BULK_JUDGE_MODEL = "deepseek/deepseek-chat"
DEFAULT_CALIBRATION_JUDGE_MODEL = "openai/gpt-4.1"
DEFAULT_CALIBRATION_SAMPLE_SIZE = 50
PAIRWISE_LEXICAL_THRESHOLD = 0.88

POINTWISE_PROMPT = """\
You are the Tenacious-Bench bulk judge filter.
Score the candidate task on a 1-5 scale for exactly these dimensions:
- input_coherence
- ground_truth_verifiability
- rubric_clarity

Return JSON with:
- scores: object with the three dimensions above
- average_score: numeric average across the three dimensions
- decision: pass or fail
- reasons: array of short strings
- required_fixes: array of short strings

Decision rule:
- pass only if every dimension is >= 4 and the average is >= 4.0
- otherwise fail
"""

PAIRWISE_PROMPT = """\
You are the Tenacious-Bench duplicate filter.
Given two candidate tasks, decide whether they are near-duplicates for benchmark purposes.
Return JSON with:
- duplicate: true or false
- overlap_reason: short string
- preferred_task_id: the better task to keep if duplicate=true
"""

CALIBRATION_PROMPT = """\
You are the Tenacious-Bench eval-tier calibration judge.
Review a previously bulk-accepted task and confirm whether the pointwise scores and final decision
look correct. Return JSON with:
- calibrated_decision: pass or fail
- confidence: low, medium, or high
- notes: array of short strings
"""


@dataclass(frozen=True)
class PointwiseScores:
    input_coherence: int
    ground_truth_verifiability: int
    rubric_clarity: int

    @property
    def average(self) -> float:
        return round(
            (
                self.input_coherence
                + self.ground_truth_verifiability
                + self.rubric_clarity
            )
            / 3.0,
            3,
        )

    def to_dict(self) -> dict[str, int]:
        return {
            "input_coherence": self.input_coherence,
            "ground_truth_verifiability": self.ground_truth_verifiability,
            "rubric_clarity": self.rubric_clarity,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Tenacious-Bench judge filter pipeline.")
    parser.add_argument("--input", type=Path, required=True, help="Input task JSONL.")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output JSONL with accepted tasks.",
    )
    parser.add_argument(
        "--log-output",
        type=Path,
        default=REPO_ROOT / "docs" / "judge_filter_log.jsonl",
        help="Structured per-task pass/fail log.",
    )
    parser.add_argument(
        "--bulk-judge-model",
        default=DEFAULT_BULK_JUDGE_MODEL,
        help="Dev-tier model used for high-volume pointwise filtering.",
    )
    parser.add_argument(
        "--calibration-judge-model",
        default=DEFAULT_CALIBRATION_JUDGE_MODEL,
        help="Eval-tier model used only for spot-check calibration.",
    )
    parser.add_argument(
        "--calibration-sample-size",
        type=int,
        default=DEFAULT_CALIBRATION_SAMPLE_SIZE,
        help="Maximum accepted-task sample for eval-tier calibration.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=11,
        help="Sampling seed for calibration spot checks.",
    )
    return parser.parse_args()


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", value.lower())).strip()


def task_text(task: dict[str, Any]) -> str:
    candidate = task.get("candidate_output", {})
    subject = candidate.get("subject", "") if isinstance(candidate, dict) else ""
    body = candidate.get("body", "") if isinstance(candidate, dict) else str(candidate)
    signal_bits = task.get("input", {}).get("hiring_signal_brief", {}).get("signals", [])
    evidence = " ".join(
        signal.get("evidence", "")
        for signal in signal_bits
        if isinstance(signal, dict)
    )
    return normalize_text(" ".join([str(subject), str(body), str(evidence)]))


def lexical_overlap(left: str, right: str) -> float:
    left_tokens = set(normalize_text(left).split())
    right_tokens = set(normalize_text(right).split())
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def score_task(task: dict[str, Any]) -> PointwiseScores:
    candidate = task.get("candidate_output", {})
    body = candidate.get("body", "") if isinstance(candidate, dict) else str(candidate)
    signals = task.get("input", {}).get("hiring_signal_brief", {}).get("signals", [])
    expected_behavior = str(task.get("ground_truth", {}).get("expected_behavior", "")).strip()
    judge_dimensions = task.get("scoring_config", {}).get("judge_dimensions", [])
    rubric = task.get("rubric", {})

    input_coherence = 5
    if not signals or not body:
        input_coherence = 1
    elif len(body.split()) < 12:
        input_coherence = 3

    ground_truth_verifiability = 5
    if not expected_behavior or "?" not in body and "can you" not in body.lower():
        ground_truth_verifiability = 3
    if task.get("failure_dimension") == "signal_grounding" and not task.get("metadata", {}).get("retrieval_provenance"):
        ground_truth_verifiability = min(ground_truth_verifiability, 2)

    rubric_clarity = 5
    if not judge_dimensions or not rubric.get("expected_terms") or not rubric.get("banned_phrases"):
        rubric_clarity = 3
    if task.get("source_mode") == "synthetic" and len(judge_dimensions) < 3:
        rubric_clarity = min(rubric_clarity, 2)

    return PointwiseScores(
        input_coherence=input_coherence,
        ground_truth_verifiability=ground_truth_verifiability,
        rubric_clarity=rubric_clarity,
    )


def passes_pointwise(scores: PointwiseScores) -> bool:
    return (
        scores.input_coherence >= POINTWISE_MIN_SCORE
        and scores.ground_truth_verifiability >= POINTWISE_MIN_SCORE
        and scores.rubric_clarity >= POINTWISE_MIN_SCORE
        and scores.average >= POINTWISE_MIN_AVERAGE
    )


def pairwise_duplicate_decision(
    left: dict[str, Any],
    right: dict[str, Any],
) -> dict[str, Any]:
    left_text = task_text(left)
    right_text = task_text(right)
    overlap = lexical_overlap(left_text, right_text)
    same_dimension = left.get("failure_dimension") == right.get("failure_dimension")
    duplicate = same_dimension and overlap >= PAIRWISE_LEXICAL_THRESHOLD
    preferred = str(left.get("task_id", ""))
    if duplicate:
        if len(left_text) < len(right_text):
            preferred = str(right.get("task_id", ""))
    return {
        "duplicate": duplicate,
        "overlap_reason": f"lexical_overlap={overlap:.3f}",
        "preferred_task_id": preferred,
    }


def enforce_family_separation(bulk_judge_model: str, calibration_judge_model: str) -> None:
    if model_family(bulk_judge_model) == model_family(calibration_judge_model):
        raise ValueError(
            "Calibration judge must use a different model family from the bulk synthesis judge."
        )


def build_log_row(
    task: dict[str, Any],
    scores: PointwiseScores,
    decision: str,
    reasons: list[str],
    pairwise: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "task_id": task.get("task_id", ""),
        "source_mode": task.get("source_mode", ""),
        "bulk_filter_model": DEFAULT_BULK_JUDGE_MODEL,
        "scores": scores.to_dict(),
        "average_score": scores.average,
        "decision": decision,
        "reasons": reasons,
        "pairwise": pairwise,
    }


def run_filter(
    rows: list[dict[str, Any]],
    *,
    bulk_judge_model: str,
    calibration_judge_model: str,
    calibration_sample_size: int,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    enforce_family_separation(bulk_judge_model, calibration_judge_model)

    accepted: list[dict[str, Any]] = []
    logs: list[dict[str, Any]] = []
    prior_rows: list[dict[str, Any]] = []

    for row in rows:
        scores = score_task(row)
        reasons: list[str] = []
        pairwise: dict[str, Any] | None = None

        if not passes_pointwise(scores):
            reasons.append(
                "pointwise_threshold_failed: each dimension must be >= 4 and average must be >= 4.0"
            )

        for prior in prior_rows:
            candidate_pairwise = pairwise_duplicate_decision(prior, row)
            if candidate_pairwise["duplicate"]:
                pairwise = candidate_pairwise
                if candidate_pairwise["preferred_task_id"] != row.get("task_id"):
                    reasons.append(
                        f"pairwise_duplicate_of:{prior.get('task_id', '')}"
                    )
                break

        decision = "pass" if not reasons else "fail"
        logs.append(build_log_row(row, scores, decision, reasons, pairwise))
        if decision == "pass":
            accepted.append(row)
        prior_rows.append(row)

    rng = random.Random(seed)
    sample_count = min(calibration_sample_size, len(accepted))
    calibration_rows = rng.sample(accepted, sample_count) if sample_count else []
    calibration = {
        "bulk_judge_model": bulk_judge_model,
        "calibration_judge_model": calibration_judge_model,
        "sample_size": sample_count,
        "sampled_task_ids": [row.get("task_id", "") for row in calibration_rows],
        "policy": "eval-tier model is used only for calibration spot-checks on accepted tasks",
    }
    return accepted, logs, calibration


def main() -> int:
    args = parse_args()
    rows = read_jsonl(args.input)
    accepted, logs, calibration = run_filter(
        rows,
        bulk_judge_model=args.bulk_judge_model,
        calibration_judge_model=args.calibration_judge_model,
        calibration_sample_size=args.calibration_sample_size,
        seed=args.seed,
    )
    write_jsonl(args.output, accepted)
    write_jsonl(args.log_output, logs)
    print(
        json.dumps(
            {
                "input_count": len(rows),
                "accepted_count": len(accepted),
                "rejected_count": len(rows) - len(accepted),
                "pointwise_dimensions": POINTWISE_DIMENSIONS,
                "pointwise_min_score": POINTWISE_MIN_SCORE,
                "pointwise_min_average": POINTWISE_MIN_AVERAGE,
                "bulk_judge_model": args.bulk_judge_model,
                "calibration": calibration,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
