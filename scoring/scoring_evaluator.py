"""Deterministic scoring smoke test for Tenacious-Bench.

This is the stable local command path used by README.md. The full task schema
will expand on these checks, but this file already returns numeric scores
without a human in the loop.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RUBRIC_DIMENSIONS = (
    "output_validity",
    "ai_maturity_consistency",
    "gap_condescension",
    "signal_grounding",
    "style_guide_adherence",
    "next_step_quality",
)

CTA_PATTERN = re.compile(
    r"\b(schedule|book|call|demo|meet|meeting|reply|send|share|next step|talk)\b",
    re.IGNORECASE,
)
CONDESCENSION_PATTERN = re.compile(
    r"\b(obviously|simply|just need to|you don't understand|basic|easy)\b",
    re.IGNORECASE,
)
AI_MATURITY_PATTERN = re.compile(r"\b(ai|automation|model|workflow|crm|sales)\b", re.IGNORECASE)


@dataclass(frozen=True)
class ScoreResult:
    scores: dict[str, float]
    passed: bool

    @property
    def total(self) -> float:
        return round(sum(self.scores.values()) / len(self.scores), 3)

    def to_dict(self) -> dict[str, Any]:
        return {"passed": self.passed, "total": self.total, "scores": self.scores}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def candidate_text(candidate: Any) -> str:
    if isinstance(candidate, str):
        return candidate
    if isinstance(candidate, dict):
        for key in ("answer", "output", "response", "message"):
            value = candidate.get(key)
            if isinstance(value, str):
                return value
    return json.dumps(candidate, sort_keys=True)


def score_candidate(task: dict[str, Any], candidate: Any) -> ScoreResult:
    text = candidate_text(candidate)
    lower_text = text.lower()
    expected_terms = [str(term).lower() for term in task.get("expected_terms", [])]
    forbidden_terms = [str(term).lower() for term in task.get("forbidden_terms", [])]

    scores = {
        "output_validity": 1.0 if text.strip() else 0.0,
        "ai_maturity_consistency": 1.0 if AI_MATURITY_PATTERN.search(text) else 0.0,
        "gap_condescension": 0.0 if CONDESCENSION_PATTERN.search(text) else 1.0,
        "signal_grounding": 1.0
        if not expected_terms or any(term in lower_text for term in expected_terms)
        else 0.0,
        "style_guide_adherence": 0.0
        if any(term in lower_text for term in forbidden_terms)
        else 1.0,
        "next_step_quality": 1.0 if CTA_PATTERN.search(text) else 0.0,
    }
    return ScoreResult(scores=scores, passed=all(value >= 1.0 for value in scores.values()))


def smoke_tasks() -> list[tuple[dict[str, Any], str]]:
    return [
        (
            {"expected_terms": ["workflow"], "forbidden_terms": ["obviously"]},
            "Your sales workflow has a clear handoff gap. Could we book a 20-minute demo to map the next step?",
        ),
        (
            {"expected_terms": ["crm"], "forbidden_terms": ["basic"]},
            "The CRM signal suggests follow-up timing is the issue. Reply with a good time for a short call.",
        ),
        (
            {"expected_terms": ["automation"], "forbidden_terms": ["just need to"]},
            "Automation can help with routing, but the buyer context matters. Can you share one recent stalled deal?",
        ),
    ]


def run_smoke() -> list[dict[str, Any]]:
    return [
        {"case": index, **score_candidate(task, candidate).to_dict()}
        for index, (task, candidate) in enumerate(smoke_tasks(), start=1)
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score a Tenacious-Bench candidate output.")
    parser.add_argument("--task", type=Path, help="Path to a task JSON file.")
    parser.add_argument("--candidate", type=Path, help="Path to a candidate output JSON or text file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.task and args.candidate:
        task = load_json(args.task)
        try:
            candidate = load_json(args.candidate)
        except json.JSONDecodeError:
            candidate = args.candidate.read_text(encoding="utf-8")
        print(json.dumps(score_candidate(task, candidate).to_dict(), indent=2, sort_keys=True))
        return 0

    results = run_smoke()
    print(json.dumps({"smoke_passed": all(item["passed"] for item in results), "results": results}, indent=2))
    return 0 if all(item["passed"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
