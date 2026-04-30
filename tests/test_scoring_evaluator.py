import unittest

from src.scoring.scoring_evaluator import score_candidate


def make_task() -> dict:
    return {
        "channel": "email",
        "rubric": {
            "expected_terms": ["workflow"],
            "forbidden_terms": [],
            "banned_phrases": [],
            "max_body_words": 120,
            "max_subject_chars": 60,
        },
        "scoring_config": {
            "deterministic_dimensions": [
                "output_nonempty",
                "subject_present_for_email",
                "max_body_words_respected",
                "max_subject_chars_respected",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ]
        },
    }


class ScoringEvaluatorTests(unittest.TestCase):
    def test_single_ask_only_rejects_bundled_asks_in_one_sentence(self) -> None:
        candidate = {
            "subject": "Question on workflow timing",
            "body": "Can you book a demo and reply with a time that works this week?",
        }
        result = score_candidate(make_task(), candidate)
        self.assertEqual(result.scores["buyer_next_step_keyword_present"], 1.0)
        self.assertEqual(result.scores["single_ask_only"], 0.0)
        self.assertFalse(result.passed)

    def test_single_ask_only_rejects_review_and_get_back_bundle(self) -> None:
        candidate = {
            "subject": "Question on workflow review",
            "body": "Please review the workflow note and get back with the owner you want involved.",
        }
        result = score_candidate(make_task(), candidate)
        self.assertEqual(result.scores["single_ask_only"], 0.0)

    def test_single_ask_only_allows_one_cta_with_call_as_context(self) -> None:
        candidate = {
            "subject": "Question on workflow follow-up",
            "body": "Can you reply with one time for a short workflow call next week?",
        }
        result = score_candidate(make_task(), candidate)
        self.assertEqual(result.scores["buyer_next_step_keyword_present"], 1.0)
        self.assertEqual(result.scores["single_ask_only"], 1.0)
        self.assertTrue(result.passed)


if __name__ == "__main__":
    unittest.main()
