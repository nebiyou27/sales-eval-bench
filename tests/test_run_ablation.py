import json
import tempfile
import unittest
from pathlib import Path

from src.ablations.run_ablation import (
    build_outcomes,
    cost_summary,
    delta_report,
    load_predictions,
    paired_bootstrap_ci,
    paired_sign_flip_p_value,
)
from src.generation.common import write_jsonl


def make_task(task_id: str) -> dict:
    return {
        "task_id": task_id,
        "partition": "held_out",
        "source_mode": "hand_authored",
        "difficulty": "hard",
        "failure_dimension": "next_step_quality",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {"company_name": "Acme", "contact_role": "COO", "company_stage": "growth"},
            "hiring_signal_brief": {
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "The buyer asked for one lightweight next step.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P34",
                    }
                ]
            },
        },
        "candidate_output": {
            "subject": "Re: one next step",
            "body": "Hi Alex, can you share one workflow artifact so we keep the next step lightweight?",
        },
        "ground_truth": {"expected_behavior": "Ask for one lightweight artifact.", "target_decision": "accept"},
        "rubric": {
            "expected_terms": ["workflow"],
            "forbidden_terms": ["schedule a call"],
            "banned_phrases": ["quick chat"],
            "max_body_words": 200,
            "max_subject_chars": 60,
        },
        "scoring_config": {"deterministic_dimensions": ["output_nonempty", "single_ask_only"]},
    }


class RunAblationTests(unittest.TestCase):
    def test_bootstrap_and_p_value_return_numbers(self) -> None:
        ci = paired_bootstrap_ci([1.0, 0.0, 1.0, 1.0], samples=200, seed=11)
        p_value = paired_sign_flip_p_value([0.2, 0.1, 0.3, 0.0], samples=200, seed=11)
        self.assertIsNotNone(ci["mean_delta"])
        self.assertIsNotNone(p_value)

    def test_build_outcomes_and_cost_summary(self) -> None:
        tasks = {"held-1": make_task("held-1")}
        predictions = {
            "held-1": {
                "task_id": "held-1",
                "passed": True,
                "total": 1.0,
                "latency_ms": 120,
                "input_tokens": 200,
                "output_tokens": 40,
                "usd_cost": 0.02,
            }
        }
        outcomes, failures = build_outcomes(tasks, predictions)
        self.assertEqual(failures, [])
        summary = cost_summary(outcomes)
        self.assertEqual(summary["task_count"], 1)
        self.assertEqual(summary["total_usd_cost"], 0.02)

    def test_delta_report_computes_lift(self) -> None:
        trained = [
            type("Outcome", (), {"task_id": "a", "passed": True, "total": 1.0})(),
            type("Outcome", (), {"task_id": "b", "passed": True, "total": 1.0})(),
        ]
        baseline = [
            type("Outcome", (), {"task_id": "a", "passed": False, "total": 0.0})(),
            type("Outcome", (), {"task_id": "b", "passed": True, "total": 1.0})(),
        ]
        report = delta_report(
            "trained_vs_baseline",
            trained,
            baseline,
            bootstrap_samples=200,
            seed=11,
        )
        self.assertEqual(report["pass_rate_lift"], 0.5)


if __name__ == "__main__":
    unittest.main()
