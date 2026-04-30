import unittest
from unittest.mock import patch

from src.generation.generate_hand_authored import HAND_AUTHORED_SPECS, materialize_tasks


class GenerateHandAuthoredTests(unittest.TestCase):
    def test_train_partition_materializes_hand_authored_tasks(self) -> None:
        tasks = materialize_tasks("train")
        self.assertEqual(len(tasks), 17)
        self.assertTrue(all(task["partition"] == "train" for task in tasks))
        self.assertTrue(all(task["source_mode"] == "hand_authored" for task in tasks))

    def test_held_out_partition_materializes_hand_authored_tasks(self) -> None:
        tasks = materialize_tasks("held_out")
        self.assertEqual(len(tasks), 30)
        self.assertTrue(all(task["partition"] == "held_out" for task in tasks))
        self.assertTrue(all(task["source_mode"] == "hand_authored" for task in tasks))

    def test_train_partition_rejects_held_out_trace_citation(self) -> None:
        patched_specs = [dict(spec) for spec in HAND_AUTHORED_SPECS]
        patched_specs[0] = dict(patched_specs[0])
        patched_specs[0]["metadata"] = dict(patched_specs[0]["metadata"])
        patched_specs[0]["metadata"]["source_trace_ids"] = ["held-out-trace-001"]

        with patch("src.generation.generate_hand_authored.HAND_AUTHORED_SPECS", patched_specs):
            with patch(
                "src.generation.generate_hand_authored.load_held_out_trace_ids",
                return_value={"held-out-trace-001"},
            ):
                with self.assertRaisesRegex(ValueError, "cites held-out trace"):
                    materialize_tasks("train")


if __name__ == "__main__":
    unittest.main()
