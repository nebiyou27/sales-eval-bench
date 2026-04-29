import unittest

from src.generation.generate_hand_authored import materialize_tasks


class GenerateHandAuthoredTests(unittest.TestCase):
    def test_train_partition_materializes_hand_authored_tasks(self) -> None:
        tasks = materialize_tasks("train")
        self.assertEqual(len(tasks), 2)
        self.assertTrue(all(task["partition"] == "train" for task in tasks))
        self.assertTrue(all(task["source_mode"] == "hand_authored" for task in tasks))

    def test_held_out_partition_materializes_hand_authored_tasks(self) -> None:
        tasks = materialize_tasks("held_out")
        self.assertEqual(len(tasks), 2)
        self.assertTrue(all(task["partition"] == "held_out" for task in tasks))
        self.assertTrue(all(task["source_mode"] == "hand_authored" for task in tasks))


if __name__ == "__main__":
    unittest.main()
