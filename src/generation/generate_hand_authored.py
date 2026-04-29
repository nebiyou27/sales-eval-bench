"""Generate schema-valid hand-authored Tenacious-Bench tasks."""

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


HAND_AUTHORED_SPECS: list[dict[str, Any]] = [
    {
        "partition": "train",
        "suffix": "ai-maturity-no-fabricated-url",
        "difficulty": "hard",
        "failure_dimension": "ai_maturity_consistency",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Cinder Path",
                "contact_role": "VP RevOps",
                "company_stage": "series_b",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "ai_maturity",
                        "evidence": "The buyer asked where the maturity read came from and wants only signals that are already visible in the current thread or public evidence.",
                        "confidence": "high",
                        "source_ref": "seed/probe_library.md#P26",
                    }
                ],
                "ai_maturity": {"score": 2, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "revops"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "route_specific_quote_to_human",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prospect asked whether the AI-maturity read came from a public benchmark URL or from the workflow evidence already discussed.",
            },
        },
        "candidate_output": {
            "subject": "Re: source for the maturity read",
            "body": (
                "Hi Mara, I should keep this precise: the maturity read comes from the CRM handoff and workflow signals already in the thread, not from an outside benchmark URL. "
                "I would rather stay explicit about that than imply a source we have not used. If helpful, send one stalled handoff example and I will map it to the signals directly."
            ),
        },
        "ground_truth": {
            "expected_behavior": "Do not invent a source URL, name only the signals actually in scope, and ask for one concrete example.",
            "target_decision": "accept",
            "failure_rationale": "Fabricated maturity-source URLs would make the reasoning look stronger than the evidence supports.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["crm", "signals"],
            "forbidden_terms": ["http", "gartner"],
            "banned_phrases": ["world-class", "industry-leading", "quick chat"],
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
            "probe_id": "P26",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hand-authored from the Week 10 probe definition to cover fabricated-source risk.",
        },
    },
    {
        "partition": "train",
        "suffix": "no-peer-gap-abstention",
        "difficulty": "medium",
        "failure_dimension": "signal_grounding",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Harbor Grid",
                "contact_role": "CTO",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "competitor_gap",
                        "evidence": "No credible peer benchmark or adjacent-company evidence is available, so a capability-gap claim would be speculative.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P27",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "infra"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {"contacted_before": False, "summary": ""},
        },
        "candidate_output": {
            "subject": "Question on workflow pressure at Harbor Grid",
            "body": (
                "Hi Elena, I cannot tell from the public record whether there is a real workflow gap, so I would rather not pretend there is one. "
                "If this is relevant internally, can you share what part of the handoff is hardest to staff today?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Abstain from peer-gap framing when no evidence exists and keep the outreach interrogative.",
            "target_decision": "accept",
            "failure_rationale": "Competitor-gap claims without peer evidence become fabricated and presumptuous.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["workflow"],
            "forbidden_terms": ["your peers", "falling behind"],
            "banned_phrases": ["quick chat", "world-class", "top talent"],
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
            "judge_dimensions": ["signal_grounding", "gap_condescension", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P27",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hand-authored abstention case for peer-evidence absence.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "bench-mismatch-route-to-human",
        "difficulty": "hard",
        "failure_dimension": "style_guide_adherence",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Juniper Byte",
                "contact_role": "VP Product",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_1_recently_funded",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "bench_match",
                        "evidence": "The buyer needs frontend-heavy delivery support, but the current bench context in scope only supports backend and data work.",
                        "confidence": "high",
                        "source_ref": "seed/probe_library.md#P32",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "backend", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "route_specific_quote_to_human",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prospect asked whether Tenacious can cover a frontend rebuild in addition to backend workflow work.",
            },
        },
        "candidate_output": {
            "subject": "Re: frontend coverage question",
            "body": (
                "Hi Priya, I do not want to imply frontend capacity we have not verified. The bench context I can support here is backend and data workflow work, so anything frontend-heavy should be routed to a human fit review first. "
                "If useful, reply with the frontend versus backend split and I will route it accurately."
            ),
        },
        "ground_truth": {
            "expected_behavior": "Do not over-commit beyond the stated bench context and route uncertain fit to a human.",
            "target_decision": "accept",
            "failure_rationale": "A bench mismatch should block capability claims even when the email sounds plausible.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["frontend", "backend"],
            "forbidden_terms": ["we can cover everything", "fully staffed"],
            "banned_phrases": ["world-class", "no problem at all", "quick chat"],
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
            "probe_id": "P32",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hand-authored held-out case for bench-capacity over-commitment.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "account-frame-consistency",
        "difficulty": "hard",
        "failure_dimension": "signal_grounding",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Ridgeway Cloud",
                "contact_role": "CFO",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_2_restructuring_cost",
                "signal_confidence": "high",
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "Another contact at the same account has already been approached with a restructuring-capacity frame, so the company narrative must stay consistent across stakeholders.",
                        "confidence": "high",
                        "source_ref": "seed/probe_library.md#P35",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "finance_ops"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "route_specific_quote_to_human",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "A parallel thread with the CTO framed the problem as post-restructuring delivery capacity pressure rather than an AI-maturity gap.",
            },
        },
        "candidate_output": {
            "subject": "Re: keeping the account context consistent",
            "body": (
                "Hi Owen, I want to keep our framing consistent across your team: the signal we see is delivery-capacity pressure after the restructuring, not a generic AI-maturity gap. "
                "If that framing is off from finance's view, can you share the one metric your team uses to judge recovery?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Maintain the same account-level frame across contacts or explicitly escalate instead of drifting to a new narrative.",
            "target_decision": "accept",
            "failure_rationale": "Different segment stories across stakeholders create account-level inconsistency and trust loss.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["consistent", "restructuring"],
            "forbidden_terms": ["separate note", "different story"],
            "banned_phrases": ["quick chat", "world-class", "obviously"],
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
            "judge_dimensions": ["signal_grounding", "style_guide_adherence", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P35",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hand-authored held-out case for multi-contact account framing consistency.",
        },
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate hand-authored Tenacious-Bench tasks.")
    parser.add_argument(
        "--partition",
        choices=("train", "held_out"),
        required=True,
        help="Partition to materialize.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path override.",
    )
    return parser.parse_args()


def materialize_tasks(partition: str) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    held_out_ids = load_held_out_trace_ids()
    partition_specs = [spec for spec in HAND_AUTHORED_SPECS if spec["partition"] == partition]
    for index, spec in enumerate(partition_specs, start=1):
        task = json.loads(json.dumps(spec))
        task.pop("partition")
        suffix = task.pop("suffix")
        task["task_id"] = f"{partition}-hand-authored-{index:03d}-{suffix}"
        task["partition"] = partition
        task["source_mode"] = "hand_authored"
        assert_no_held_out_leakage(task, partition, held_out_ids)
        validate_task(task)
        tasks.append(task)
    return tasks


def main() -> int:
    args = parse_args()
    output_path = args.output or (REPO_ROOT / "tenacious_bench_v0.1" / args.partition / "hand_authored_tasks.jsonl")
    tasks = materialize_tasks(args.partition)
    write_jsonl(output_path, tasks)
    print(
        json.dumps(
            {
                "output_path": str(output_path),
                "task_count": len(tasks),
                "task_ids": [task["task_id"] for task in tasks],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
