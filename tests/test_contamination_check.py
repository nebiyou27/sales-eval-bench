import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.generation.common import write_jsonl
from src.generation.contamination_check import build_report


def make_task(task_id: str, partition: str, source_mode: str = "hand_authored") -> dict:
    return {
        "task_id": task_id,
        "partition": partition,
        "source_mode": source_mode,
        "difficulty": "medium",
        "failure_dimension": "signal_grounding",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {"company_name": "Acme", "contact_role": "CTO", "company_stage": "growth"},
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "competitor_gap",
                        "evidence": f"Evidence for {task_id}",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P33",
                    }
                ],
                "ai_maturity": {"score": 2, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {"contacted_before": True, "summary": "Thread summary"},
        },
        "candidate_output": {"subject": "Re: note", "body": f"Candidate output for {task_id}"},
        "ground_truth": {"expected_behavior": "Stay grounded.", "target_decision": "accept"},
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["candidate"],
            "forbidden_terms": ["obviously"],
            "banned_phrases": ["world-class"],
            "max_body_words": 200,
            "max_subject_chars": 60,
            "one_ask_required": True,
            "require_signal_reference": True,
            "confidence_aware_language": True,
            "forbid_bench_term": True,
            "allowed_channels": ["email"],
        },
        "scoring_config": {
            "deterministic_dimensions": [
                "output_nonempty",
                "subject_present_for_email",
                "max_body_words_respected",
                "max_subject_chars_respected",
            ],
            "judge_dimensions": ["signal_grounding"],
        },
        "metadata": {
            "probe_id": "P33",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
        },
    }


class ContaminationCheckTests(unittest.TestCase):
    def test_embedding_status_is_honest_when_model_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset_root = Path(temp_dir)
            write_jsonl(dataset_root / "train" / "train_tasks.jsonl", [make_task("train-001", "train")])
            write_jsonl(dataset_root / "held_out" / "held_tasks.jsonl", [make_task("held-001", "held_out")])
            report = build_report(dataset_root, "missing-local-model")
        self.assertTrue(report["embedding_check_status"].startswith("embedding_check_unavailable:"))
        self.assertEqual(report["embedding_model"], "missing-local-model")

    def test_embedding_findings_use_real_embedding_scores_when_available(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset_root = Path(temp_dir)
            write_jsonl(dataset_root / "train" / "train_tasks.jsonl", [make_task("train-001", "train")])
            write_jsonl(dataset_root / "held_out" / "held_tasks.jsonl", [make_task("held-001", "held_out")])
            with patch(
                "src.generation.contamination_check.encode_texts",
                return_value=[[1.0, 0.0], [0.99, 0.01]],
            ):
                report = build_report(dataset_root, "stub-model")
        self.assertEqual(report["embedding_check_status"], "embedding_check_completed")
        self.assertEqual(len(report["overlap_findings"]), 1)
        self.assertIn("embedding_cosine", report["overlap_findings"][0])


if __name__ == "__main__":
    unittest.main()
