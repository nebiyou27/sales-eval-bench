import unittest

from src.generation.generate_synthesis import build_prompt_manifest, dedup_key


class GenerateSynthesisTests(unittest.TestCase):
    def test_build_prompt_manifest_stamps_incrementing_seeds(self) -> None:
        manifest = build_prompt_manifest(
            partition="dev",
            generation_model="qwen/qwen3-next-80b-a3b-instruct",
            judge_model="deepseek/deepseek-chat",
            seed=41,
        )

        self.assertGreaterEqual(len(manifest), 3)
        self.assertEqual(manifest[0]["generation_seed"], 41)
        self.assertEqual(manifest[1]["generation_seed"], 42)
        self.assertEqual(manifest[2]["generation_seed"], 43)

    def test_dedup_key_normalizes_case_spacing_and_punctuation(self) -> None:
        left = {
            "failure_dimension": "signal_grounding",
            "channel": "email",
            "message_kind": "cold_outreach",
            "candidate_output": {
                "subject": "Question on Workflow Load",
                "body": "Hi Rafael,\nA few public hiring signals are visible.",
            },
        }
        right = {
            "failure_dimension": "signal_grounding",
            "channel": "EMAIL",
            "message_kind": "cold_outreach",
            "candidate_output": {
                "subject": " question on workflow load ",
                "body": "Hi Rafael,   A few public hiring signals are visible!",
            },
        }

        self.assertEqual(dedup_key(left), dedup_key(right))


if __name__ == "__main__":
    unittest.main()
