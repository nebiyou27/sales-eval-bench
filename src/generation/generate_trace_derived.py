"""Generate schema-valid trace-derived Tenacious-Bench tasks.

The Week 10 seed traces available in this repo expose trace IDs and rewards, but
not the original prompt/output payloads. To keep provenance honest, this script
materializes tasks from an explicit audited mapping of known trace IDs to
Tenacious-specific failure-mode templates. It also hard-blocks any held-out
trace IDs from entering train/dev partitions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import (
    REPO_ROOT,
    assert_no_held_out_leakage,
    load_held_out_trace_ids,
    read_jsonl,
    validate_task,
    write_jsonl,
)


TRACE_DERIVED_SPECS: list[dict[str, Any]] = [
    {
        "trace_id": "a553180f-80d2-4d4b-9a1e-d525b1219cfd",
        "task_id_suffix": "competitor-gap-restraint",
        "difficulty": "hard",
        "failure_dimension": "gap_condescension",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Northbeam Commerce",
                "contact_role": "CTO",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "competitor_gap",
                        "evidence": "Two adjacent commerce-tooling peers posted MLOps roles; no equivalent public hiring signal is visible for the prospect.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P33",
                    }
                ],
                "ai_maturity": {"score": 2, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "ml"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {"contacted_before": False, "summary": ""},
        },
        "candidate_output": {
            "subject": "Question on MLOps scope at Northbeam",
            "body": (
                "Hi Rina, two adjacent commerce-platform teams recently staffed MLOps roles while your public signals stay quieter. "
                "That may reflect a deliberate architecture choice rather than a gap. If useful, would you be open to a short call to compare "
                "what those teams appear to be automating versus what you prefer to keep manual?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Frame the peer comparison as research, avoid condescension, and keep the ask low-pressure.",
            "target_decision": "accept",
            "failure_rationale": "The audited trace showed competitor-gap outreach can become intrusive when the buyer is technically sophisticated.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional", "non_condescending"],
            "expected_terms": ["manual"],
            "forbidden_terms": ["behind the curve", "you need to", "basic"],
            "banned_phrases": ["world-class", "quick chat", "falling behind"],
            "max_body_words": 120,
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
                "banned_phrase_absent",
                "bench_term_absent",
                "banned_condescension_absent",
                "expected_signal_term_present",
                "forbidden_terms_absent",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ],
            "judge_dimensions": ["gap_condescension", "signal_grounding", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P33",
            "source_artifact": "seed/trace_log.jsonl",
            "style_guide_version": "v2",
            "source_trace_ids": ["a553180f-80d2-4d4b-9a1e-d525b1219cfd"],
            "trace_reward": 0.0,
            "derivation_note": "Task reconstructed from audited failed trace metadata and Week 10 probe evidence; original payload not copied into repo.",
        },
    },
    {
        "trace_id": "89337dd1-bb36-41d7-8530-190df8734cc3",
        "task_id_suffix": "ai-maturity-structured-visibility",
        "difficulty": "hard",
        "failure_dimension": "ai_maturity_consistency",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "SignalArc",
                "contact_role": "VP Data",
                "company_stage": "series_b",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "high",
                "signals": [
                    {
                        "signal_type": "ai_maturity",
                        "evidence": "The prospect wants AI-maturity reasoning that keeps each signal legible instead of collapsing into prose or blank output.",
                        "confidence": "high",
                        "source_ref": "seed/probe_library.md#P24",
                    }
                ],
                "ai_maturity": {"score": 2, "confidence": "high"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "route_specific_quote_to_human",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prospect asked for a concrete explanation of how the maturity read was formed.",
            },
        },
        "candidate_output": {
            "subject": "Re: maturity-signal breakdown",
            "body": (
                "Hi Noor, the maturity read is not a capability claim by itself. The visible CRM instrumentation and workflow ownership signals suggest "
                "an intermediate state, but I would rather keep the confidence explicit than overstate it. If helpful, reply with one example of where "
                "handoffs stall and I can map it to the signals we are using."
            ),
        },
        "ground_truth": {
            "expected_behavior": "Keep the maturity reasoning usable and confidence-aware, then ask for one concrete clarifying example.",
            "target_decision": "accept",
            "failure_rationale": "The audited trace reflected AI-maturity reasoning that became unusable when the model lost structure.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["crm", "signals"],
            "forbidden_terms": ["obviously", "just need to"],
            "banned_phrases": ["world-class", "i hope this email finds you well"],
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
                "ai_maturity_keyword_present",
                "banned_phrase_absent",
                "bench_term_absent",
                "banned_condescension_absent",
                "expected_signal_term_present",
                "forbidden_terms_absent",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ],
            "judge_dimensions": ["ai_maturity_consistency", "signal_grounding", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P24",
            "source_artifact": "seed/trace_log.jsonl",
            "style_guide_version": "v2",
            "source_trace_ids": ["89337dd1-bb36-41d7-8530-190df8734cc3"],
            "trace_reward": 0.0,
            "derivation_note": "Task reconstructed from audited failed trace metadata and Week 10 probe evidence; original payload not copied into repo.",
        },
    },
    {
        "trace_id": "0857ba6e-d8cb-4ec8-b024-3d5ddc298fc6",
        "task_id_suffix": "demo-boundary-honesty",
        "difficulty": "medium",
        "failure_dimension": "style_guide_adherence",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "RelayForge",
                "contact_role": "Head of Platform",
                "company_stage": "series_b",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "The buyer is checking whether a previous artifact represented live behavior or a fixture-backed review run.",
                        "confidence": "high",
                        "source_ref": "seed/probe_library.md#P30",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "infra"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "route_specific_quote_to_human",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prospect asked whether the artifact they saw came from a fixture-backed review path.",
            },
        },
        "candidate_output": {
            "subject": "Re: artifact provenance",
            "body": (
                "Hi Dana, that artifact came from a fixture-backed review path rather than a live production run. I want to keep that boundary explicit before "
                "we discuss any capability implication. If useful, I can send the review checklist we use before anything moves from fixture-backed "
                "evidence into production-safe language."
            ),
        },
        "ground_truth": {
            "expected_behavior": "State the demo boundary plainly, avoid production overclaim, and offer one concrete follow-up.",
            "target_decision": "accept",
            "failure_rationale": "The audited trace represents the trust loss that occurs when fixture-backed artifacts are presented as live evidence.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["fixture-backed"],
            "forbidden_terms": ["production-ready"],
            "banned_phrases": ["quick chat", "do not miss out"],
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
                "banned_phrase_absent",
                "bench_term_absent",
                "expected_signal_term_present",
                "forbidden_terms_absent",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ],
            "judge_dimensions": ["style_guide_adherence", "signal_grounding", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P30",
            "source_artifact": "seed/trace_log.jsonl",
            "style_guide_version": "v2",
            "source_trace_ids": ["0857ba6e-d8cb-4ec8-b024-3d5ddc298fc6"],
            "trace_reward": 0.0,
            "derivation_note": "Task reconstructed from audited failed trace metadata and Week 10 probe evidence; original payload not copied into repo.",
        },
    },
    {
        "trace_id": "19d13ac9-f495-4df4-b1c4-d042ca754933",
        "task_id_suffix": "thin-evidence-restraint",
        "difficulty": "easy",
        "failure_dimension": "output_validity",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "MeridianOps",
                "contact_role": "VP Operations",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_2_restructuring_cost",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "job_post_velocity",
                        "evidence": "A small number of public roles exist, but there is not enough evidence to claim a broad staffing bottleneck.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P29",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {"contacted_before": False, "summary": ""},
        },
        "candidate_output": {
            "subject": "Question on workflow load at MeridianOps",
            "body": (
                "Hi Jess, I can see a few public hiring signals, but not enough to say whether they reflect a real workflow bottleneck or normal backfill. "
                "If the load is higher than it appears from the outside, can you share one example where the queue slows down today?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Use low-confidence language, avoid unsupported claims, and ask for one example only.",
            "target_decision": "accept",
            "failure_rationale": "The audited trace stands in for weak-signal situations where unsupported outreach should abstain or stay interrogative.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["queue"],
            "forbidden_terms": ["obviously", "clearly"],
            "banned_phrases": ["quick question", "world-class", "synergize"],
            "max_body_words": 120,
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
                "banned_phrase_absent",
                "bench_term_absent",
                "banned_condescension_absent",
                "expected_signal_term_present",
                "forbidden_terms_absent",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ],
            "judge_dimensions": ["output_validity", "signal_grounding", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P29",
            "source_artifact": "seed/trace_log.jsonl",
            "style_guide_version": "v2",
            "source_trace_ids": ["19d13ac9-f495-4df4-b1c4-d042ca754933"],
            "trace_reward": 0.0,
            "derivation_note": "Task reconstructed from audited failed trace metadata and Week 10 probe evidence; original payload not copied into repo.",
        },
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate trace-derived Tenacious-Bench tasks.")
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "tenacious_bench_v0.1" / "dev" / "trace_derived_tasks.jsonl",
        help="Where to write the generated tasks JSONL.",
    )
    parser.add_argument(
        "--partition",
        choices=("train", "dev"),
        default="dev",
        help="Partition label to stamp onto the generated tasks. Held-out traces remain excluded.",
    )
    parser.add_argument(
        "--trace-log",
        type=Path,
        default=REPO_ROOT / "seed" / "trace_log.jsonl",
        help="Week 10 trace metadata source.",
    )
    parser.add_argument(
        "--held-out-traces",
        type=Path,
        default=REPO_ROOT / "seed" / "held_out_traces.jsonl",
        help="Held-out trace metadata used only for leakage prevention.",
    )
    return parser.parse_args()


def trace_index(path: Path) -> dict[str, dict[str, Any]]:
    return {row["simulation_id"]: row for row in read_jsonl(path) if "simulation_id" in row}


def materialize_tasks(
    partition: str,
    trace_rows: dict[str, dict[str, Any]],
    held_out_ids: set[str],
) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for index, spec in enumerate(TRACE_DERIVED_SPECS, start=1):
        trace_id = spec["trace_id"]
        if trace_id not in trace_rows:
            raise ValueError(f"Trace {trace_id} was not found in {REPO_ROOT / 'seed' / 'trace_log.jsonl'}.")

        trace_row = trace_rows[trace_id]
        expected_reward = spec["metadata"]["trace_reward"]
        actual_reward = trace_row.get("reward")
        if actual_reward != expected_reward:
            raise ValueError(
                f"Trace {trace_id} reward mismatch: expected {expected_reward}, found {actual_reward}."
            )

        task = json.loads(json.dumps(spec))
        task.pop("trace_id")
        suffix = task.pop("task_id_suffix")
        task["task_id"] = f"{partition}-trace-derived-{index:03d}-{suffix}"
        task["partition"] = partition
        task["source_mode"] = "trace_derived"
        task["metadata"]["original_task_id"] = str(trace_row.get("task_id", ""))
        task["metadata"]["trace_domain"] = str(trace_row.get("domain", ""))
        task["metadata"]["trace_termination_reason"] = str(trace_row.get("termination_reason", ""))
        validate_task(task)
        assert_no_held_out_leakage(task, partition, held_out_ids)
        tasks.append(task)
    return tasks


def main() -> int:
    args = parse_args()
    trace_rows = trace_index(args.trace_log)
    held_out_ids = load_held_out_trace_ids(args.held_out_traces)
    tasks = materialize_tasks(args.partition, trace_rows, held_out_ids)
    write_jsonl(args.output, tasks)
    print(
        json.dumps(
            {
                "output_path": str(args.output),
                "task_count": len(tasks),
                "task_ids": [task["task_id"] for task in tasks],
                "source_trace_ids": [
                    task["metadata"]["source_trace_ids"][0]
                    for task in tasks
                ],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
