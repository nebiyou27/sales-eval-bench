import unittest

from src.generation.judge_filter import (
    PointwiseScores,
    pairwise_duplicate_decision,
    passes_pointwise,
    run_filter,
)


def make_task(task_id: str, body: str, *, source_mode: str = "synthetic") -> dict:
    return {
        "task_id": task_id,
        "partition": "train",
        "source_mode": source_mode,
        "difficulty": "hard",
        "failure_dimension": "signal_grounding",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {"company_name": "Acme", "contact_role": "CTO", "company_stage": "growth"},
            "hiring_signal_brief": {
                "signals": [
                    {
                        "signal_type": "job_post_velocity",
                        "evidence": "A stale public signal needs explicit confidence marking.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P05",
                    }
                ]
            },
        },
        "candidate_output": {
            "subject": "Question on workflow signal",
            "body": body,
        },
        "ground_truth": {
            "expected_behavior": "Keep the claim grounded and ask one question.",
            "target_decision": "accept",
        },
        "rubric": {
            "expected_terms": ["workflow", "signal"],
            "forbidden_terms": ["obviously"],
            "banned_phrases": ["world-class", "quick chat"],
        },
        "scoring_config": {
            "judge_dimensions": ["signal_grounding", "next_step_quality", "style_guide_adherence"],
        },
        "metadata": {
            "probe_id": "P05",
            "retrieval_provenance": {
                "url": "https://example.com",
                "retrieved_at": "2026-04-30T00:00:00Z",
                "source_type": "press_release",
            },
        },
    }


class JudgeFilterTests(unittest.TestCase):
    def test_passes_pointwise_requires_each_dimension_and_average_threshold(self) -> None:
        self.assertTrue(passes_pointwise(PointwiseScores(4, 4, 4)))
        self.assertFalse(passes_pointwise(PointwiseScores(5, 5, 3)))

    def test_pairwise_duplicate_logic_flags_near_duplicates(self) -> None:
        left = make_task(
            "task-1",
            "Hi Dana, the workflow signal is stale and low confidence. Can you share one current workflow example?",
        )
        right = make_task(
            "task-2",
            "Hi Dana, the workflow signal is stale and low confidence. Can you share one current workflow example?",
        )
        result = pairwise_duplicate_decision(left, right)
        self.assertTrue(result["duplicate"])

    def test_run_filter_logs_failures_and_accepts_only_passing_rows(self) -> None:
        accepted, logs, calibration = run_filter(
            [
                make_task(
                    "task-pass",
                    "Hi Dana, the workflow signal is low confidence and still grounded. Can you share one workflow example?",
                ),
                make_task("task-fail", "Too short."),
            ],
            bulk_judge_model="deepseek/deepseek-chat",
            calibration_judge_model="openai/gpt-4.1",
            calibration_sample_size=50,
            seed=11,
        )
        self.assertEqual([row["task_id"] for row in accepted], ["task-pass"])
        self.assertEqual(len(logs), 2)
        self.assertEqual(calibration["sample_size"], 1)


if __name__ == "__main__":
    unittest.main()
