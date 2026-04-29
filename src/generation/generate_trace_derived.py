"""Generate schema-valid trace-derived Tenacious-Bench tasks for Act II wave 1.

The seed traces in this repo expose only audited trace metadata, not the full
prompt/output payloads. This script expands each allowed trace into a larger
family of provenance-honest train/dev tasks while still blocking held-out IDs.
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


PROSPECTS: list[dict[str, str]] = [
    {"company_name": "Northbeam Commerce", "contact_role": "CTO", "company_stage": "growth", "first_name": "Rina"},
    {"company_name": "SignalArc", "contact_role": "VP Data", "company_stage": "series_b", "first_name": "Noor"},
    {"company_name": "RelayForge", "contact_role": "Head of Platform", "company_stage": "series_b", "first_name": "Dana"},
    {"company_name": "MeridianOps", "contact_role": "VP Operations", "company_stage": "mid_market", "first_name": "Jess"},
    {"company_name": "Helix", "contact_role": "CTO", "company_stage": "mid_market", "first_name": "Felix"},
    {"company_name": "LoyaltyStack", "contact_role": "CTO", "company_stage": "series_b", "first_name": "Kevin"},
    {"company_name": "Juniper Lake", "contact_role": "VP Revenue Systems", "company_stage": "growth", "first_name": "Mina"},
    {"company_name": "QuarryOS", "contact_role": "COO", "company_stage": "mid_market", "first_name": "Rafael"},
    {"company_name": "Atlas CRM", "contact_role": "VP Engineering", "company_stage": "series_b", "first_name": "Camila"},
    {"company_name": "Northstar Health", "contact_role": "VP Data", "company_stage": "mid_market", "first_name": "Tom"},
    {"company_name": "Blue Current", "contact_role": "Head of Revenue Ops", "company_stage": "growth", "first_name": "Avery"},
    {"company_name": "Driftwell", "contact_role": "VP Platform", "company_stage": "series_b", "first_name": "Leah"},
    {"company_name": "Cinder Data", "contact_role": "VP Analytics", "company_stage": "mid_market", "first_name": "Omar"},
    {"company_name": "Pine Harbor", "contact_role": "CTO", "company_stage": "growth", "first_name": "Erin"},
    {"company_name": "Riverglass", "contact_role": "Head of Systems", "company_stage": "series_b", "first_name": "Gabe"},
]

TRACE_DERIVED_BLUEPRINTS: list[dict[str, Any]] = [
    {
        "trace_id": "a553180f-80d2-4d4b-9a1e-d525b1219cfd",
        "suffix": "competitor-gap-restraint",
        "probe_id": "P33",
        "failure_dimension": "gap_condescension",
        "difficulty": "hard",
        "signal_type": "competitor_gap",
        "primary_segment": "segment_4_capability_gap",
        "signal_confidence": "medium",
        "ai_score": 2,
        "ai_confidence": "medium",
        "supported_stacks": ["python", "data", "ml"],
        "pricing_scope": "public_bands_only",
        "source_ref": "seed/probe_library.md#P33",
        "expected_terms": ["manual", "workflow"],
        "forbidden_terms": ["behind the curve", "you need to", "basic"],
        "banned_phrases": ["world-class", "quick chat", "falling behind"],
        "tone_markers": ["direct", "grounded", "honest", "professional", "non_condescending"],
        "judge_dimensions": ["gap_condescension", "signal_grounding", "next_step_quality"],
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
        "target_decision": "accept",
        "expected_behavior": "Use the audited peer-gap trace as respectful research, not as a maturity lecture.",
        "failure_rationale": "Sophisticated buyers should not receive simplistic or patronizing gap language.",
        "subject_stems": [
            "Question on workflow coverage",
            "Question on peer automation scope",
            "Question on MLOps tradeoffs",
        ],
        "evidence_templates": [
            "Adjacent teams staffed MLOps roles, but that public difference may reflect a deliberate workflow choice rather than a gap.",
            "The trace-derived peer signal is useful only if it stays framed as optional workflow research.",
            "A quieter hiring pattern can still be intentional, especially when manual workflow ownership is part of the design.",
        ],
        "ask_templates": [
            "Can you reply with one workflow area you prefer to keep manual so the comparison stays respectful?",
            "Can you share whether those peer MLOps postings map to work you have deliberately not prioritized?",
            "Can you send one example where peer automation differs from your preferred workflow model?",
        ],
        "prior_thread_templates": [
            "The buyer asked us to keep the peer comparison practical rather than presumptuous.",
            "The prospect wants outside evidence framed as research, not as a basic maturity lesson.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "email", "email", "linkedin_dm", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
        },
        "message_kinds": {
            "train": ["cold_outreach", "cold_outreach", "cold_outreach", "reengagement", "cold_outreach", "reengagement", "cold_outreach", "reengagement", "cold_outreach"],
            "dev": ["cold_outreach", "cold_outreach", "reengagement", "cold_outreach", "cold_outreach", "reengagement"],
        },
    },
    {
        "trace_id": "89337dd1-bb36-41d7-8530-190df8734cc3",
        "suffix": "ai-maturity-structured-visibility",
        "probe_id": "P24",
        "failure_dimension": "ai_maturity_consistency",
        "difficulty": "hard",
        "signal_type": "ai_maturity",
        "primary_segment": "segment_4_capability_gap",
        "signal_confidence": "high",
        "ai_score": 2,
        "ai_confidence": "high",
        "supported_stacks": ["python", "data"],
        "pricing_scope": "route_specific_quote_to_human",
        "source_ref": "seed/probe_library.md#P24",
        "expected_terms": ["workflow", "signal"],
        "forbidden_terms": ["obviously", "just need to"],
        "banned_phrases": ["world-class", "i hope this email finds you well"],
        "tone_markers": ["direct", "grounded", "honest", "professional"],
        "judge_dimensions": ["ai_maturity_consistency", "signal_grounding", "next_step_quality"],
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
        "target_decision": "accept",
        "expected_behavior": "Keep maturity signals structured, confidence-aware, and tied to a single grounded follow-up.",
        "failure_rationale": "The trace represents how AI-maturity reasoning becomes unusable when structure is lost.",
        "subject_stems": [
            "Re: maturity signal review",
            "Re: CRM signal breakdown",
            "Re: workflow maturity note",
        ],
        "evidence_templates": [
            "The CRM instrumentation and workflow ownership signals should stay explicit instead of collapsing into generic prose.",
            "The maturity read is useful only when the visible signals and the confidence level remain legible together.",
            "A structured automation signal is safer than a flattened capability claim.",
        ],
        "ask_templates": [
            "Can you reply with one example where the workflow handoff stalls so the maturity read stays grounded?",
            "Can you share one CRM bottleneck that would let us test the visible signals against a real workflow?",
            "Can you send one operational example that would sharpen the confidence on the maturity read?",
        ],
        "prior_thread_templates": [
            "The buyer asked for a concrete explanation of how the maturity signal was formed.",
            "The prospect wants the workflow reasoning to stay structured instead of abstract.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "email", "email", "linkedin_dm", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
        },
        "message_kinds": {
            "train": ["warm_reply", "warm_reply", "reengagement", "warm_reply", "reengagement", "warm_reply", "warm_reply", "reengagement", "warm_reply"],
            "dev": ["warm_reply", "reengagement", "warm_reply", "warm_reply", "warm_reply", "reengagement"],
        },
    },
    {
        "trace_id": "0857ba6e-d8cb-4ec8-b024-3d5ddc298fc6",
        "suffix": "demo-boundary-honesty",
        "probe_id": "P30",
        "failure_dimension": "style_guide_adherence",
        "difficulty": "medium",
        "signal_type": "prior_thread",
        "primary_segment": "segment_4_capability_gap",
        "signal_confidence": "medium",
        "ai_score": 1,
        "ai_confidence": "medium",
        "supported_stacks": ["python", "infra"],
        "pricing_scope": "route_specific_quote_to_human",
        "source_ref": "seed/probe_library.md#P30",
        "expected_terms": ["fixture-backed", "production"],
        "forbidden_terms": ["production-ready"],
        "banned_phrases": ["quick chat", "do not miss out"],
        "tone_markers": ["direct", "grounded", "honest", "professional"],
        "judge_dimensions": ["style_guide_adherence", "signal_grounding", "next_step_quality"],
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
        "target_decision": "accept",
        "expected_behavior": "Name the fixture or demo boundary plainly before any production implication.",
        "failure_rationale": "Artifact provenance needs to stay explicit to preserve reviewer trust.",
        "subject_stems": [
            "Re: artifact provenance",
            "Re: fixture-backed review path",
            "Re: production evidence question",
        ],
        "evidence_templates": [
            "The artifact came from a fixture-backed review path rather than a live production run.",
            "The safest phrasing is to keep the fixture-backed boundary explicit before discussing any production implication.",
            "Production language should wait until the review artifact is labeled honestly.",
        ],
        "ask_templates": [
            "Can you reply if the production-safe review checklist would be more useful than another artifact?",
            "Can you share which artifact detail still needs a production-safe answer?",
            "Can you send the exact provenance question that still feels unresolved?",
        ],
        "prior_thread_templates": [
            "The prospect asked whether the earlier artifact represented a live run or a fixture-backed review path.",
            "The buyer is checking whether the artifact should be treated as production evidence.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "email", "linkedin_dm", "linkedin_dm", "linkedin_dm", "sms"],
            "dev": ["email", "email", "email", "linkedin_dm", "linkedin_dm", "sms"],
        },
        "message_kinds": {
            "train": ["warm_reply", "warm_reply", "reengagement", "warm_reply", "reengagement", "warm_reply", "reengagement", "warm_reply", "warm_reply"],
            "dev": ["warm_reply", "reengagement", "warm_reply", "warm_reply", "reengagement", "warm_reply"],
        },
    },
    {
        "trace_id": "19d13ac9-f495-4df4-b1c4-d042ca754933",
        "suffix": "thin-evidence-restraint",
        "probe_id": "P29",
        "failure_dimension": "output_validity",
        "difficulty": "easy",
        "signal_type": "job_post_velocity",
        "primary_segment": "segment_2_restructuring_cost",
        "signal_confidence": "low",
        "ai_score": 1,
        "ai_confidence": "medium",
        "supported_stacks": ["python", "data"],
        "pricing_scope": "public_bands_only",
        "source_ref": "seed/probe_library.md#P29",
        "expected_terms": ["queue", "workflow"],
        "forbidden_terms": ["obviously", "clearly"],
        "banned_phrases": ["quick question", "world-class", "synergize"],
        "tone_markers": ["direct", "grounded", "honest", "professional"],
        "judge_dimensions": ["output_validity", "signal_grounding", "next_step_quality"],
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
        "target_decision": "accept",
        "expected_behavior": "Stay specific and well-formed when the visible signal only supports an abstaining posture.",
        "failure_rationale": "Thin-evidence drafts often degrade into generic filler instead of a usable restrained note.",
        "subject_stems": [
            "Question on workflow load",
            "Checking the queue signal",
            "Question on the visible hiring pattern",
        ],
        "evidence_templates": [
            "A small number of public signals are visible, but they still do not prove a real workflow queue problem.",
            "The trace-derived signal may reflect routine backfill, so the note should stay restrained instead of generic.",
            "The cleanest output is a short workflow note that is explicit about what the public signal cannot prove.",
        ],
        "ask_templates": [
            "Can you reply with one queue example if the outside workflow signal is missing something material?",
            "Can you share one workflow bottleneck if the public hiring signal understates the real pressure?",
            "Can you send one example that would make the queue signal more concrete?",
        ],
        "prior_thread_templates": [
            "The buyer asked for a shorter follow-up that stays concrete rather than generic.",
            "The prospect confirmed SMS follow-up is okay if the message stays restrained and specific.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "email", "linkedin_dm", "linkedin_dm", "linkedin_dm", "sms"],
            "dev": ["email", "email", "email", "linkedin_dm", "linkedin_dm", "sms"],
        },
        "message_kinds": {
            "train": ["cold_outreach", "reengagement", "cold_outreach", "cold_outreach", "reengagement", "cold_outreach", "reengagement", "cold_outreach", "warm_reply"],
            "dev": ["cold_outreach", "reengagement", "cold_outreach", "cold_outreach", "reengagement", "warm_reply"],
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


def sentence_for(options: list[str], index: int) -> str:
    return options[index % len(options)]


def trace_index(path: Path) -> dict[str, dict[str, Any]]:
    return {row["simulation_id"]: row for row in read_jsonl(path) if "simulation_id" in row}


def prior_thread_for(channel: str, message_kind: str, blueprint: dict[str, Any], index: int) -> dict[str, Any]:
    contacted_before = channel == "sms" or message_kind != "cold_outreach"
    if not contacted_before:
        return {"contacted_before": False, "summary": ""}
    summary = sentence_for(blueprint["prior_thread_templates"], index)
    if channel == "sms":
        summary = f"{summary} The prospect explicitly confirmed SMS follow-up is okay after the earlier thread."
    return {"contacted_before": True, "summary": summary}


def candidate_output_for(
    blueprint: dict[str, Any],
    prospect: dict[str, str],
    channel: str,
    message_kind: str,
    index: int,
) -> dict[str, str]:
    intro = sentence_for(blueprint["evidence_templates"], index)
    ask = sentence_for(blueprint["ask_templates"], index)
    greeting = f"Hi {prospect['first_name']}, "
    if channel == "sms":
        return {"body": f"{greeting}{intro} {ask}"}
    if channel == "linkedin_dm":
        return {"body": f"{greeting}{intro} {ask}"}

    prefix = "Re: " if message_kind != "cold_outreach" else ""
    subject = f"{prefix}{sentence_for(blueprint['subject_stems'], index)}"
    return {"subject": subject[:60], "body": f"{greeting}{intro} {ask}"}


def max_body_words_for(message_kind: str) -> int:
    if message_kind == "cold_outreach":
        return 120
    if message_kind == "reengagement":
        return 100
    return 200


def materialize_tasks(
    partition: str,
    trace_rows: dict[str, dict[str, Any]],
    held_out_ids: set[str],
) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for blueprint_index, blueprint in enumerate(TRACE_DERIVED_BLUEPRINTS, start=1):
        trace_id = blueprint["trace_id"]
        if trace_id not in trace_rows:
            raise ValueError(f"Trace {trace_id} was not found in {REPO_ROOT / 'seed' / 'trace_log.jsonl'}.")
        trace_row = trace_rows[trace_id]
        actual_reward = trace_row.get("reward")
        if actual_reward != 0.0:
            raise ValueError(f"Trace {trace_id} reward mismatch: expected 0.0, found {actual_reward}.")

        channels = blueprint["channels"][partition]
        message_kinds = blueprint["message_kinds"][partition]
        if len(channels) != len(message_kinds):
            raise ValueError(f"Channel/message plan mismatch for {blueprint['suffix']} {partition}.")

        for variant_index, channel in enumerate(channels):
            message_kind = message_kinds[variant_index]
            prospect = PROSPECTS[(blueprint_index * 4 + variant_index) % len(PROSPECTS)]
            task_index = len(tasks) + 1
            candidate_output = candidate_output_for(
                blueprint,
                prospect,
                channel,
                message_kind,
                variant_index,
            )
            task = {
                "task_id": f"{partition}-trace-derived-{task_index:03d}-{blueprint['suffix']}",
                "partition": partition,
                "source_mode": "trace_derived",
                "difficulty": blueprint["difficulty"],
                "failure_dimension": blueprint["failure_dimension"],
                "channel": channel,
                "message_kind": message_kind,
                "input": {
                    "prospect": {
                        "company_name": prospect["company_name"],
                        "contact_role": prospect["contact_role"],
                        "company_stage": prospect["company_stage"],
                    },
                    "hiring_signal_brief": {
                        "primary_segment": blueprint["primary_segment"],
                        "signal_confidence": blueprint["signal_confidence"],
                        "signals": [
                            {
                                "signal_type": blueprint["signal_type"],
                                "evidence": sentence_for(blueprint["evidence_templates"], variant_index),
                                "confidence": blueprint["signal_confidence"],
                                "source_ref": blueprint["source_ref"],
                            }
                        ],
                        "ai_maturity": {
                            "score": blueprint["ai_score"],
                            "confidence": blueprint["ai_confidence"],
                        },
                    },
                    "bench_context": {
                        "supported_stacks": blueprint["supported_stacks"],
                        "capacity_commitment_allowed": False,
                        "pricing_scope": blueprint["pricing_scope"],
                    },
                    "prior_thread": prior_thread_for(channel, message_kind, blueprint, variant_index),
                },
                "candidate_output": candidate_output,
                "ground_truth": {
                    "expected_behavior": blueprint["expected_behavior"],
                    "target_decision": blueprint["target_decision"],
                    "failure_rationale": blueprint["failure_rationale"],
                },
                "rubric": {
                    "tone_markers": blueprint["tone_markers"],
                    "expected_terms": blueprint["expected_terms"],
                    "forbidden_terms": blueprint["forbidden_terms"],
                    "banned_phrases": blueprint["banned_phrases"],
                    "max_body_words": max_body_words_for(message_kind),
                    "one_ask_required": True,
                    "require_signal_reference": True,
                    "confidence_aware_language": True,
                    "forbid_bench_term": True,
                    "allowed_channels": [channel],
                    **({"max_subject_chars": 60} if channel == "email" else {}),
                },
                "scoring_config": {
                    "deterministic_dimensions": blueprint["deterministic_dimensions"],
                    "judge_dimensions": blueprint["judge_dimensions"],
                },
                "metadata": {
                    "probe_id": blueprint["probe_id"],
                    "source_artifact": "seed/trace_log.jsonl",
                    "style_guide_version": "v2",
                    "source_trace_ids": [trace_id],
                    "trace_reward": 0.0,
                    "derivation_note": "Task reconstructed from audited failed trace metadata and Week 10 probe evidence; original payload not copied into repo.",
                    "original_task_id": str(trace_row.get("task_id", "")),
                    "trace_domain": str(trace_row.get("domain", "")),
                    "trace_termination_reason": str(trace_row.get("termination_reason", "")),
                },
            }
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
                "source_trace_ids": [task["metadata"]["source_trace_ids"][0] for task in tasks],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
