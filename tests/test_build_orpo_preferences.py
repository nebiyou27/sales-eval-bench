import tempfile
import unittest
from pathlib import Path

from src.generation.common import write_jsonl
from src.training.build_orpo_preferences import (
    LOCAL_REJECTED_MODEL,
    build_preference_seed,
    load_public_tasks,
    validate_seed_record,
)
from src.training.validate_orpo_preferences import validate_row


def sample_task(partition: str = "train", source_mode: str = "programmatic") -> dict:
    return {
        "task_id": f"{partition}-task-001",
        "partition": partition,
        "source_mode": source_mode,
        "difficulty": "medium",
        "failure_dimension": "style_guide_adherence",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Helix",
                "contact_role": "CTO",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "The buyer wants scope labels kept explicit.",
                        "confidence": "low",
                    }
                ]
            },
            "prior_thread": {"summary": "The buyer asked for clearer scope labeling."},
        },
        "candidate_output": {
            "subject": "Re: review scope note",
            "body": "Hi Felix, I will keep the review scope explicit. Can you reply with one artifact that still needs a scope label?",
        },
        "ground_truth": {
            "expected_behavior": "Keep review scope explicit and grounded.",
            "target_decision": "accept",
        },
        "rubric": {
            "expected_terms": ["scope", "review"],
            "forbidden_terms": ["production-ready"],
            "banned_phrases": ["quick chat", "world-class"],
        },
        "scoring_config": {
            "deterministic_dimensions": ["output_nonempty"],
            "judge_dimensions": ["style_guide_adherence", "signal_grounding"],
        },
        "metadata": {
            "probe_id": "P30",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
        },
    }


class BuildOrpoPreferencesTests(unittest.TestCase):
    def test_load_public_tasks_excludes_held_out_partition(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset_root = Path(temp_dir)
            write_jsonl(dataset_root / "train" / "tasks.jsonl", [sample_task("train")])
            write_jsonl(dataset_root / "dev" / "tasks.jsonl", [sample_task("dev")])
            write_jsonl(dataset_root / "held_out" / "tasks.jsonl", [sample_task("held_out")])

            tasks = load_public_tasks(dataset_root)

        self.assertEqual(len(tasks), 2)
        self.assertEqual({task["partition"] for task in tasks}, {"train", "dev"})

    def test_build_preference_seed_populates_required_fields(self) -> None:
        row = build_preference_seed(sample_task())
        self.assertEqual(row["source_task_id"], "train-task-001")
        self.assertEqual(row["chosen_source"], "benchmark_candidate_output")
        self.assertEqual(row["rejected_source"], "style_guide_bad_example")
        self.assertEqual(row["rejected_model"], LOCAL_REJECTED_MODEL)
        validate_seed_record(row)

    def test_validate_row_rejects_held_out_source_partition(self) -> None:
        row = build_preference_seed(sample_task())
        row["source_partition"] = "held_out"
        errors = validate_row(row, {"train-task-001": "train"})
        self.assertTrue(any("held_out" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
