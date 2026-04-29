"""Generate schema-valid programmatic Tenacious-Bench tasks.

This script expands a small, explicit set of Tenacious-specific templates into
benchmark tasks. It is meant to be deterministic, cheap, and easy to inspect.
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
    validate_task,
    write_jsonl,
)


PROGRAMMATIC_TEMPLATES: list[dict[str, Any]] = [
    {
        "suffix": "ai-maturity-structured-reply",
        "difficulty": "hard",
        "failure_dimension": "ai_maturity_consistency",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Atlas CRM",
                "contact_role": "VP Engineering",
                "company_stage": "series_b",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_1_recently_funded",
                "signal_confidence": "high",
                "signals": [
                    {
                        "signal_type": "ai_maturity",
                        "evidence": "The AI maturity scorer must preserve CRM and automation signals in a usable, JSON-valid form.",
                        "confidence": "high",
                        "source_ref": "seed/failure_taxonomy.md#P24",
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
                "summary": "The prospect replied asking for a more concrete next step tied to CRM workflow issues.",
            },
        },
        "candidate_output": {
            "subject": "Re: workflow handoff question",
            "body": (
                "Hi Camila, the CRM and AI maturity signals point to a workflow handoff issue rather than a capability claim. "
                "Please reply with one stalled deal example so we can choose the next step without inventing unsupported reasons."
            ),
        },
        "ground_truth": {
            "expected_behavior": "Preserve AI-maturity context in a usable form, avoid invented claims, and end with one concrete next step.",
            "target_decision": "accept",
            "failure_rationale": "Invalid or unstructured AI-maturity reasoning should be revised or blocked.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["crm"],
            "forbidden_terms": ["just need to"],
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
            "source_artifact": "seed/failure_taxonomy.md",
            "style_guide_version": "v2",
            "source_trace_ids": ["92995764-0b20-48cd-8121-0b4641a7858b"],
        },
    },
    {
        "suffix": "thin-signal-question",
        "difficulty": "easy",
        "failure_dimension": "signal_grounding",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Northstar Health",
                "contact_role": "VP Data",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_2_restructuring_cost",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "job_post_velocity",
                        "evidence": "Two public data-engineer roles are visible; signal is too weak to assert aggressive scaling.",
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
            "subject": "Question: are your data hires keeping up?",
            "body": (
                "Hi Tom, I can see two public data-engineer roles, but I cannot tell from the outside "
                "whether that means the queue is longer than the postings suggest. If the real demand "
                "is higher, can we book 15 minutes to compare it with the current workflow bottleneck?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Use interrogative language on weak evidence and make only one ask.",
            "target_decision": "accept",
            "failure_rationale": "Thin evidence should trigger restraint, not a scaling claim.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["workflow"],
            "forbidden_terms": ["obviously"],
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
            "judge_dimensions": ["signal_grounding", "style_guide_adherence", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P29",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "source_trace_ids": ["19d13ac9-f495-4df4-b1c4-d042ca754933"],
        },
    },
    {
        "suffix": "fixture-live-boundary",
        "difficulty": "medium",
        "failure_dimension": "style_guide_adherence",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "LoyaltyStack",
                "contact_role": "CTO",
                "company_stage": "series_b",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "The prospect asked whether a previous demo artifact reflected production behavior.",
                        "confidence": "high",
                        "source_ref": "seed/probe_library.md#P30",
                    }
                ],
                "ai_maturity": {"score": 2, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "ml", "infra"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "route_specific_quote_to_human",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prospect is asking whether a previous artifact was a demo-mode run or production output.",
            },
        },
        "candidate_output": {
            "subject": "Re: demo artifact question",
            "body": (
                "Hi Kevin, that artifact was from a demo-mode run, not production output. I wanted to be explicit "
                "about the fixture/live boundary before we discuss any next step. If useful, I can send the production-safe "
                "criteria we use before a workflow is presented externally."
            ),
        },
        "ground_truth": {
            "expected_behavior": "Name demo mode explicitly, avoid overstating the artifact, and offer one low-friction next step.",
            "target_decision": "accept",
            "failure_rationale": "Demo artifacts must not be represented as live production evidence.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["demo-mode"],
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
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "source_trace_ids": ["0857ba6e-d8cb-4ec8-b024-3d5ddc298fc6"],
        },
    },
    {
        "suffix": "competitor-gap-research-frame",
        "difficulty": "hard",
        "failure_dimension": "gap_condescension",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Helix",
                "contact_role": "CTO",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "high",
                "signals": [
                    {
                        "signal_type": "competitor_gap",
                        "evidence": "Three adjacent loyalty-platform companies posted senior MLOps roles in the last 90 days; the prospect did not.",
                        "confidence": "high",
                        "source_ref": "seed/probe_library.md#P33",
                    }
                ],
                "ai_maturity": {"score": 2, "confidence": "high"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "ml", "infra"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {"contacted_before": False, "summary": ""},
        },
        "candidate_output": {
            "subject": "Question: your MLOps function in 2026",
            "body": (
                "Hi Felix, three adjacent loyalty-platform teams posted senior MLOps roles in the last 90 days while your "
                "public signals do not show the same function yet. That may be a deliberate choice rather than a gap. If you "
                "want, can we take 15 minutes to compare what those peer teams appear to be scoping?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Frame the capability difference as a research finding or question, not a personal failing.",
            "target_decision": "accept",
            "failure_rationale": "Competitor-gap evidence should not become condescending outreach.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional", "non_condescending"],
            "expected_terms": ["mlops"],
            "forbidden_terms": ["behind the curve", "you need to", "falling behind"],
            "banned_phrases": ["world-class", "top talent", "quick chat"],
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
                "ai_maturity_keyword_present",
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
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "source_trace_ids": ["a553180f-80d2-4d4b-9a1e-d525b1219cfd"],
        },
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate programmatic Tenacious-Bench tasks.")
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "tenacious_bench_v0.1" / "dev" / "programmatic_tasks.jsonl",
        help="Where to write the generated tasks JSONL.",
    )
    parser.add_argument(
        "--partition",
        choices=("train", "dev", "held_out"),
        default="dev",
        help="Partition label to stamp onto the generated tasks.",
    )
    return parser.parse_args()


def materialize_tasks(partition: str) -> list[dict[str, Any]]:
    held_out_ids = load_held_out_trace_ids()
    tasks: list[dict[str, Any]] = []
    for index, template in enumerate(PROGRAMMATIC_TEMPLATES, start=1):
        task = json.loads(json.dumps(template))
        suffix = task.pop("suffix")
        task["task_id"] = f"{partition}-programmatic-{index:03d}-{suffix}"
        task["partition"] = partition
        task["source_mode"] = "programmatic"
        validate_task(task)
        assert_no_held_out_leakage(task, partition, held_out_ids)
        tasks.append(task)
    return tasks


def main() -> int:
    args = parse_args()
    tasks = materialize_tasks(args.partition)
    write_jsonl(args.output, tasks)
    print(
        json.dumps(
            {
                "output_path": str(args.output),
                "task_count": len(tasks),
                "task_ids": [task["task_id"] for task in tasks],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
