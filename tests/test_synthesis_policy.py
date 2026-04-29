import unittest

from src.generation.synthesis_policy import enforce_rotation, model_family


class SynthesisPolicyTests(unittest.TestCase):
    def test_model_family_normalizes_common_providers(self) -> None:
        self.assertEqual(model_family("qwen/qwen3-next-80b-a3b-instruct"), "qwen")
        self.assertEqual(model_family("deepseek/deepseek-chat"), "deepseek")
        self.assertEqual(model_family("claude-3-7-sonnet"), "claude")
        self.assertEqual(model_family("gpt-4.1-mini"), "gpt")

    def test_rotation_rejects_same_family(self) -> None:
        with self.assertRaises(ValueError):
            enforce_rotation("qwen/qwen3-next-80b-a3b-instruct", "qwen/qwen2.5-72b-instruct")

    def test_rotation_allows_distinct_families(self) -> None:
        enforce_rotation("qwen/qwen3-next-80b-a3b-instruct", "deepseek/deepseek-chat")


if __name__ == "__main__":
    unittest.main()
