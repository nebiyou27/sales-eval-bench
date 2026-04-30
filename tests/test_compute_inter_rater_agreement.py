import unittest

from src.scoring.compute_inter_rater_agreement import compute_agreement, validate_subset


DIMENSIONS = (
    "gap_condescension",
    "ai_maturity_consistency",
    "output_validity",
    "signal_grounding",
    "style_guide_adherence",
    "next_step_quality",
)


def make_row(index: int, dimension: str) -> dict:
    return {
        "task_id": f"dev-test-{index:03d}",
        "partition": "dev",
        "failure_dimension": dimension,
        "difficulty": "medium",
        "source_mode": "programmatic",
        "channel": "email",
        "message_kind": "warm_reply",
        "candidate_output": {"subject": "Subject", "body": "Body"},
        "ground_truth": {"target_decision": "accept"},
        "rubric": {},
        "judge_dimensions": [dimension],
        "deterministic_baseline": {"scores": {}, "passed": True},
        "human_agreement": {
            "first_pass_label": {dimension: ""},
            "second_pass_label": {dimension: ""},
            "second_labeler_label": {dimension: ""},
            "agreement_status": {dimension: ""},
            "notes": {dimension: ""},
            "scheduled_second_pass_at": "2026-05-01",
        },
    }


class ComputeInterRaterAgreementTests(unittest.TestCase):
    def test_validate_subset_accepts_30_dev_rows_with_5_per_dimension(self) -> None:
        rows = []
        index = 1
        for dimension in DIMENSIONS:
            for _ in range(5):
                rows.append(make_row(index, dimension))
                index += 1
        self.assertEqual(validate_subset(rows), [])

    def test_compute_agreement_flags_below_threshold_and_pending_pairs(self) -> None:
        rows = [make_row(index, "gap_condescension") for index in range(1, 6)]
        rows[0]["human_agreement"]["first_pass_label"]["gap_condescension"] = "pass"
        rows[0]["human_agreement"]["second_pass_label"]["gap_condescension"] = "pass"
        rows[0]["human_agreement"]["second_labeler_label"]["gap_condescension"] = "fail"
        rows[1]["human_agreement"]["first_pass_label"]["gap_condescension"] = "pass"
        rows[1]["human_agreement"]["second_pass_label"]["gap_condescension"] = "fail"
        rows[1]["human_agreement"]["second_labeler_label"]["gap_condescension"] = "pass"

        summary = compute_agreement(rows, threshold=0.8)
        test_retest = summary["gap_condescension"]["test_retest"]
        inter_rater = summary["gap_condescension"]["inter_rater"]

        self.assertEqual(test_retest["completed_pairs"], 2)
        self.assertEqual(test_retest["pending_pairs"], 3)
        self.assertEqual(test_retest["matches"], 1)
        self.assertEqual(test_retest["agreement_rate"], 0.5)
        self.assertTrue(test_retest["below_threshold"])

        self.assertEqual(inter_rater["completed_pairs"], 2)
        self.assertEqual(inter_rater["matches"], 1)
        self.assertEqual(inter_rater["agreement_rate"], 0.5)
        self.assertTrue(inter_rater["below_threshold"])


if __name__ == "__main__":
    unittest.main()
