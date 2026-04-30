import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.generation.common import write_jsonl
from src.training.prepare_orpo_data import (
    build_summary,
    index_dataset_tasks,
    main,
    prepare_preference_record,
    prepare_records,
    validate_preference_pair_rotation,
)


def populate_dataset_root(dataset_root: Path) -> None:
    write_jsonl(
        dataset_root / "train" / "tasks.jsonl",
        [
            {"task_id": "train-task-001", "partition": "train"},
            {"task_id": "train-task-002", "partition": "train"},
        ],
    )
    write_jsonl(
        dataset_root / "dev" / "tasks.jsonl",
        [{"task_id": "dev-task-001", "partition": "dev"}],
    )
    write_jsonl(
        dataset_root / "held_out" / "tasks.jsonl",
        [{"task_id": "held-task-001", "partition": "held_out"}],
    )


def make_record() -> dict:
    return {
        "id": "pair-001",
        "prompt": "Write a grounded reply.",
        "chosen": "Here is a grounded reply.",
        "rejected": "Here is an unsafe reply.",
        "source_task_id": "train-task-001",
        "source_partition": "train",
        "metadata": {"rejected_model": "qwen/qwen2.5-72b-instruct"},
    }


class PrepareOrpoDataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dataset_root = Path(self.temp_dir.name)
        populate_dataset_root(self.dataset_root)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_validate_preference_pair_rotation_rejects_same_family_judge_for_rejected_model(self) -> None:
        with self.assertRaisesRegex(ValueError, "same model family"):
            validate_preference_pair_rotation(
                "deepseek/deepseek-chat",
                "qwen/qwen3-next-80b-a3b-instruct",
                "deepseek/deepseek-reasoner",
            )

    def test_prepare_preference_record_stamps_rotation_and_source_metadata(self) -> None:
        prepared = prepare_preference_record(
            make_record(),
            task_index=index_dataset_tasks(self.dataset_root),
            chosen_rewrite_model="qwen/qwen3-next-80b-a3b-instruct",
            chosen_rewrite_judge_model="deepseek/deepseek-chat",
        )
        self.assertEqual(prepared["output_partition"], "train")
        self.assertEqual(prepared["source_task_id"], "train-task-001")
        self.assertEqual(prepared["source_partition"], "train")
        self.assertEqual(
            prepared["metadata"]["chosen_rewrite_model"],
            "qwen/qwen3-next-80b-a3b-instruct",
        )
        self.assertEqual(
            prepared["metadata"]["chosen_rewrite_judge_model"],
            "deepseek/deepseek-chat",
        )

    def test_index_dataset_tasks_excludes_held_out_partition(self) -> None:
        task_index = index_dataset_tasks(self.dataset_root)
        self.assertEqual(task_index["train-task-001"], "train")
        self.assertEqual(task_index["dev-task-001"], "dev")
        self.assertNotIn("held-task-001", task_index)

    def test_prepare_preference_record_requires_rejected_model_for_rotation(self) -> None:
        record = make_record()
        record["metadata"] = {}
        with self.assertRaisesRegex(ValueError, "missing rejected_model"):
            prepare_preference_record(
                record,
                task_index=index_dataset_tasks(self.dataset_root),
                chosen_rewrite_model="qwen/qwen3-next-80b-a3b-instruct",
                chosen_rewrite_judge_model="deepseek/deepseek-chat",
            )

    def test_prepare_preference_record_rejects_identical_chosen_and_rejected(self) -> None:
        record = make_record()
        record["rejected"] = record["chosen"]
        with self.assertRaisesRegex(ValueError, "identical chosen and rejected"):
            prepare_preference_record(
                record,
                task_index=index_dataset_tasks(self.dataset_root),
                chosen_rewrite_model="qwen/qwen3-next-80b-a3b-instruct",
                chosen_rewrite_judge_model="deepseek/deepseek-chat",
            )

    def test_prepare_preference_record_rejects_held_out_source_partition(self) -> None:
        record = make_record()
        record["source_task_id"] = "held-task-001"
        record["source_partition"] = "held_out"
        with self.assertRaisesRegex(ValueError, "held_out source_task_id"):
            prepare_preference_record(
                record,
                task_index=index_dataset_tasks(self.dataset_root),
                chosen_rewrite_model="qwen/qwen3-next-80b-a3b-instruct",
                chosen_rewrite_judge_model="deepseek/deepseek-chat",
            )

    def test_prepare_preference_record_rejects_mismatched_source_partition(self) -> None:
        record = make_record()
        record["source_partition"] = "dev"
        with self.assertRaisesRegex(ValueError, "claims source_partition=dev"):
            prepare_preference_record(
                record,
                task_index=index_dataset_tasks(self.dataset_root),
                chosen_rewrite_model="qwen/qwen3-next-80b-a3b-instruct",
                chosen_rewrite_judge_model="deepseek/deepseek-chat",
            )

    def test_prepare_records_collects_drops_for_summary(self) -> None:
        valid = make_record()
        invalid = make_record()
        invalid["id"] = "pair-002"
        invalid["source_task_id"] = "held-task-001"
        invalid["source_partition"] = "held_out"
        prepared_rows, dropped_rows = prepare_records(
            [valid, invalid],
            task_index=index_dataset_tasks(self.dataset_root),
            chosen_rewrite_model="qwen/qwen3-next-80b-a3b-instruct",
            chosen_rewrite_judge_model="deepseek/deepseek-chat",
        )
        self.assertEqual(len(prepared_rows), 1)
        self.assertEqual(len(dropped_rows), 1)
        self.assertEqual(dropped_rows[0]["id"], "pair-002")

    def test_build_summary_reports_kept_and_dropped_counts(self) -> None:
        summary = build_summary(
            input_path=Path("in.jsonl"),
            output_path=Path("out.jsonl"),
            dataset_root=Path("dataset"),
            input_count=3,
            prepared_count=2,
            dropped_rows=[{"id": "pair-003", "reason": "bad"}],
            chosen_rewrite_model="qwen/qwen3-next-80b-a3b-instruct",
            chosen_rewrite_judge_model="deepseek/deepseek-chat",
            dry_run=True,
            strict=False,
        )
        self.assertEqual(summary["prepared_count"], 2)
        self.assertEqual(summary["dropped_count"], 1)
        self.assertTrue(summary["dry_run"])
        self.assertFalse(summary["strict"])

    def test_main_dry_run_prints_summary_and_skips_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.jsonl"
            output_path = Path(temp_dir) / "output.jsonl"
            write_jsonl(input_path, [make_record()])
            stdout = io.StringIO()
            with patch(
                "sys.argv",
                [
                    "prepare_orpo_data.py",
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                    "--dataset-root",
                    str(self.dataset_root),
                    "--dry-run",
                ],
            ):
                with patch("sys.stdout", stdout):
                    exit_code = main()
        summary = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(summary["prepared_count"], 1)
        self.assertFalse(output_path.exists())

    def test_main_non_strict_writes_partial_success_and_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.jsonl"
            output_path = Path(temp_dir) / "output.jsonl"
            valid = make_record()
            invalid = make_record()
            invalid["id"] = "pair-002"
            invalid["source_task_id"] = "held-task-001"
            invalid["source_partition"] = "held_out"
            write_jsonl(input_path, [valid, invalid])
            stdout = io.StringIO()
            with patch(
                "sys.argv",
                [
                    "prepare_orpo_data.py",
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                    "--dataset-root",
                    str(self.dataset_root),
                ],
            ):
                with patch("sys.stdout", stdout):
                    exit_code = main()
            summary = json.loads(stdout.getvalue())
            written_rows = [
                json.loads(line)
                for line in output_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        self.assertEqual(exit_code, 0)
        self.assertEqual(summary["prepared_count"], 1)
        self.assertEqual(summary["dropped_count"], 1)
        self.assertEqual(len(written_rows), 1)

    def test_main_strict_returns_nonzero_when_rows_are_dropped(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.jsonl"
            output_path = Path(temp_dir) / "output.jsonl"
            valid = make_record()
            invalid = make_record()
            invalid["id"] = "pair-002"
            invalid["source_task_id"] = "held-task-001"
            invalid["source_partition"] = "held_out"
            write_jsonl(input_path, [valid, invalid])
            stdout = io.StringIO()
            with patch(
                "sys.argv",
                [
                    "prepare_orpo_data.py",
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                    "--dataset-root",
                    str(self.dataset_root),
                    "--strict",
                ],
            ):
                with patch("sys.stdout", stdout):
                    exit_code = main()
        summary = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 1)
        self.assertEqual(summary["prepared_count"], 1)
        self.assertEqual(summary["dropped_count"], 1)


if __name__ == "__main__":
    unittest.main()
