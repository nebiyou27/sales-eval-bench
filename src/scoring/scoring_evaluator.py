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


DETERMINISTIC_CHECKS = (
    "output_nonempty",
    "subject_present_for_email",
    "max_body_words_respected",
    "max_subject_chars_respected",
    "ai_maturity_keyword_present",
    "banned_phrase_absent",
    "bench_term_absent",
    "banned_condescension_absent",
    "expected_signal_term_present",
    "forbidden_terms_absent",
    "buyer_next_step_keyword_present",
    "single_ask_only",
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
BENCH_PATTERN = re.compile(r"\bbench\b", re.IGNORECASE)


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
        subject = candidate.get("subject")
        body = candidate.get("body")
        if isinstance(subject, str) or isinstance(body, str):
            parts = [part for part in (subject, body) if isinstance(part, str) and part.strip()]
            if parts:
                return "\n".join(parts)
        for key in ("answer", "output", "response", "message"):
            value = candidate.get(key)
            if isinstance(value, str):
                return value
    return json.dumps(candidate, sort_keys=True)


def candidate_subject(candidate: Any) -> str:
    if isinstance(candidate, dict):
        subject = candidate.get("subject")
        if isinstance(subject, str):
            return subject
    return ""


def candidate_body(candidate: Any) -> str:
    if isinstance(candidate, dict):
        body = candidate.get("body")
        if isinstance(body, str):
            return body
    return candidate_text(candidate)


def score_candidate(task: dict[str, Any], candidate: Any) -> ScoreResult:
    text = candidate_text(candidate)
    body = candidate_body(candidate)
    subject = candidate_subject(candidate)
    lower_text = text.lower()
    rubric = task.get("rubric", task)
    channel = task.get("channel", "")
    expected_terms = [str(term).lower() for term in rubric.get("expected_terms", [])]
    forbidden_terms = [str(term).lower() for term in rubric.get("forbidden_terms", [])]
    banned_phrases = [str(term).lower() for term in rubric.get("banned_phrases", [])]
    body_words = len(re.findall(r"\S+", body))
    max_body_words = rubric.get("max_body_words")
    max_subject_chars = rubric.get("max_subject_chars")
    cta_sentences = [
        sentence for sentence in re.split(r"(?<=[.!?])\s+", text) if CTA_PATTERN.search(sentence)
    ]

    scores = {
        "output_nonempty": 1.0 if text.strip() else 0.0,
        "subject_present_for_email": 1.0
        if channel != "email" or subject.strip()
        else 0.0,
        "max_body_words_respected": 1.0
        if not isinstance(max_body_words, int) or body_words <= max_body_words
        else 0.0,
        "max_subject_chars_respected": 1.0
        if channel != "email"
        or not isinstance(max_subject_chars, int)
        or len(subject) <= max_subject_chars
        else 0.0,
        "ai_maturity_keyword_present": 1.0 if AI_MATURITY_PATTERN.search(text) else 0.0,
        "banned_phrase_absent": 0.0
        if any(term in lower_text for term in banned_phrases)
        else 1.0,
        "bench_term_absent": 0.0 if BENCH_PATTERN.search(text) else 1.0,
        "banned_condescension_absent": 0.0 if CONDESCENSION_PATTERN.search(text) else 1.0,
        "expected_signal_term_present": 1.0
        if not expected_terms or any(term in lower_text for term in expected_terms)
        else 0.0,
        "forbidden_terms_absent": 0.0
        if any(term in lower_text for term in forbidden_terms)
        else 1.0,
        "buyer_next_step_keyword_present": 1.0 if CTA_PATTERN.search(text) else 0.0,
        "single_ask_only": 1.0 if len(cta_sentences) <= 1 else 0.0,
    }
    deterministic_dimensions = task.get("scoring_config", {}).get(
        "deterministic_dimensions", DETERMINISTIC_CHECKS
    )
    selected_scores = {
        dimension: scores[dimension]
        for dimension in deterministic_dimensions
        if dimension in scores
    }
    return ScoreResult(
        scores=selected_scores,
        passed=all(value >= 1.0 for value in selected_scores.values()),
    )


def smoke_tasks() -> list[tuple[dict[str, Any], str, bool]]:
    return [
        (
            {
                "channel": "email",
                "rubric": {
                    "expected_terms": ["workflow"],
                    "forbidden_terms": ["obviously"],
                    "banned_phrases": [],
                    "max_body_words": 120,
                    "max_subject_chars": 60,
                },
            },
            {
                "subject": "Request: workflow handoff question",
                "body": "Your sales workflow has a clear handoff gap. Could we book a 20-minute demo to map the next step?",
            },
            True,
        ),
        (
            {
                "channel": "email",
                "rubric": {
                    "expected_terms": ["crm"],
                    "forbidden_terms": ["basic"],
                    "banned_phrases": [],
                    "max_body_words": 200,
                    "max_subject_chars": 60,
                },
            },
            {
                "subject": "Re: CRM workflow question",
                "body": "The CRM signal suggests follow-up timing is the issue. Reply with a good time for a short call.",
            },
            True,
        ),
        (
            {
                "channel": "email",
                "rubric": {
                    "expected_terms": ["automation"],
                    "forbidden_terms": ["just need to"],
                    "banned_phrases": [],
                    "max_body_words": 120,
                    "max_subject_chars": 60,
                },
            },
            {
                "subject": "Question: routing bottleneck",
                "body": "Automation can help with routing, but the buyer context matters. Can you share one recent stalled deal?",
            },
            True,
        ),
        (
            {
                "channel": "email",
                "rubric": {
                    "expected_terms": ["workflow"],
                    "forbidden_terms": ["obviously"],
                    "banned_phrases": [],
                    "max_body_words": 120,
                    "max_subject_chars": 60,
                },
            },
            {"subject": "Question: workflow gap", "body": "You obviously need basic monitoring."},
            False,
        ),
        (
            {
                "channel": "email",
                "rubric": {
                    "expected_terms": ["crm"],
                    "forbidden_terms": [],
                    "banned_phrases": [],
                    "max_body_words": 200,
                    "max_subject_chars": 60,
                },
            },
            {"subject": "Re: CRM note", "body": ""},
            False,
        ),
    ]


def run_smoke() -> list[dict[str, Any]]:
    results = []
    for index, (task, candidate, expected_pass) in enumerate(smoke_tasks(), start=1):
        result = score_candidate(task, candidate).to_dict()
        result["case"] = index
        result["expected_pass"] = expected_pass
        result["matched_expectation"] = result["passed"] == expected_pass
        results.append(result)
    return results


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

    if args.task:
        task = load_json(args.task)
        candidate = task.get("candidate_output", "")
        print(json.dumps(score_candidate(task, candidate).to_dict(), indent=2, sort_keys=True))
        return 0

    results = run_smoke()
    smoke_passed = all(item["matched_expectation"] for item in results)
    print(json.dumps({"smoke_passed": smoke_passed, "results": results}, indent=2))
    return 0 if smoke_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
