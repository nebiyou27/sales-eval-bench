"""Generate schema-valid programmatic Tenacious-Bench tasks for Act II wave 1.

This script expands a small set of audited failure-mode blueprints into a larger
deterministic train/dev corpus without touching held-out.
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


PROSPECTS: list[dict[str, str]] = [
    {"company_name": "Atlas CRM", "contact_role": "VP Engineering", "company_stage": "series_b", "first_name": "Camila"},
    {"company_name": "Northstar Health", "contact_role": "VP Data", "company_stage": "mid_market", "first_name": "Tom"},
    {"company_name": "LoyaltyStack", "contact_role": "CTO", "company_stage": "series_b", "first_name": "Kevin"},
    {"company_name": "Helix", "contact_role": "CTO", "company_stage": "mid_market", "first_name": "Felix"},
    {"company_name": "RelayForge", "contact_role": "Head of Platform", "company_stage": "series_b", "first_name": "Dana"},
    {"company_name": "Juniper Lake", "contact_role": "VP Revenue Systems", "company_stage": "growth", "first_name": "Mina"},
    {"company_name": "QuarryOS", "contact_role": "COO", "company_stage": "mid_market", "first_name": "Rafael"},
    {"company_name": "SignalArc", "contact_role": "VP Data", "company_stage": "series_b", "first_name": "Noor"},
    {"company_name": "Northbeam Commerce", "contact_role": "CTO", "company_stage": "growth", "first_name": "Rina"},
    {"company_name": "MeridianOps", "contact_role": "VP Operations", "company_stage": "mid_market", "first_name": "Jess"},
]

PROGRAMMATIC_BLUEPRINTS: list[dict[str, Any]] = [
    {
        "suffix": "ai-maturity-structured-reply",
        "probe_id": "P24",
        "failure_dimension": "ai_maturity_consistency",
        "difficulty": "hard",
        "signal_type": "ai_maturity",
        "primary_segment": "segment_1_recently_funded",
        "signal_confidence": "high",
        "ai_score": 2,
        "ai_confidence": "high",
        "supported_stacks": ["python", "data"],
        "pricing_scope": "route_specific_quote_to_human",
        "source_ref": "seed/failure_taxonomy.md#P24",
        "source_trace_ids": ["92995764-0b20-48cd-8121-0b4641a7858b"],
        "expected_terms": ["crm", "workflow"],
        "forbidden_terms": ["just need to"],
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
        "expected_behavior": "Keep AI-maturity reasoning legible, confidence-aware, and tied to one grounded next step.",
        "failure_rationale": "Malformed or flattened maturity reasoning should be revised before outreach.",
        "subject_stems": [
            "Re: workflow signal review",
            "Re: CRM handoff signal",
            "Re: maturity reasoning check",
        ],
        "evidence_templates": [
            "The visible CRM workflow still points to an intermediate automation state rather than a broad capability claim.",
            "The automation signal is useful only if the CRM and workflow context stay explicit instead of collapsing into prose.",
            "The maturity read is usable because the workflow signal and the confidence level remain visible together.",
        ],
        "ask_templates": [
            "Can you reply with one stalled handoff so we can keep the workflow diagnosis grounded?",
            "Can you share one CRM bottleneck that would let us test the maturity read against a real workflow?",
            "Can you send one example where the automation handoff breaks down today?",
        ],
        "prior_thread_templates": [
            "The prospect asked for a more concrete explanation of the CRM workflow reasoning.",
            "The buyer replied asking how the maturity read connects to a real workflow bottleneck.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "email", "linkedin_dm"],
        },
        "message_kinds": {
            "train": ["warm_reply", "warm_reply", "reengagement", "warm_reply", "warm_reply", "reengagement"],
            "dev": ["warm_reply", "reengagement", "warm_reply", "warm_reply"],
        },
    },
    {
        "suffix": "thin-signal-restraint",
        "probe_id": "P29",
        "failure_dimension": "signal_grounding",
        "difficulty": "easy",
        "signal_type": "job_post_velocity",
        "primary_segment": "segment_2_restructuring_cost",
        "signal_confidence": "low",
        "ai_score": 1,
        "ai_confidence": "medium",
        "supported_stacks": ["python", "data"],
        "pricing_scope": "public_bands_only",
        "source_ref": "seed/probe_library.md#P29",
        "source_trace_ids": [],
        "expected_terms": ["workflow", "queue"],
        "forbidden_terms": ["obviously"],
        "banned_phrases": ["quick question", "world-class", "synergize"],
        "tone_markers": ["direct", "grounded", "honest", "professional"],
        "judge_dimensions": ["signal_grounding", "style_guide_adherence", "next_step_quality"],
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
        "expected_behavior": "Use interrogative, low-confidence language when the visible signal is thin.",
        "failure_rationale": "Weak public evidence should not become a confident prospect narrative.",
        "subject_stems": [
            "Question on workflow load",
            "Checking the queue signal",
            "Question on hiring signal confidence",
        ],
        "evidence_templates": [
            "A few public hiring signals are visible, but they are still too thin to claim a real workflow queue issue.",
            "The hiring signal may reflect routine backfill rather than a true workflow bottleneck.",
            "From the outside the queue signal stays ambiguous, so the language should remain interrogative.",
        ],
        "ask_templates": [
            "Can you share one place where the workflow queue actually slows down if the outside signal is missing something?",
            "Can you reply with one example if the hiring signal understates the real workflow pressure?",
            "Can you send one case where the queue is heavier than the public signal suggests?",
        ],
        "prior_thread_templates": [
            "The prospect replied after a prior note and confirmed SMS follow-up is okay if the framing stays grounded.",
            "The buyer asked us not to over-interpret the public hiring signal without a concrete example.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "linkedin_dm", "sms"],
        },
        "message_kinds": {
            "train": ["cold_outreach", "cold_outreach", "cold_outreach", "reengagement", "cold_outreach", "reengagement"],
            "dev": ["cold_outreach", "reengagement", "cold_outreach", "warm_reply"],
        },
    },
    {
        "suffix": "fixture-live-boundary",
        "probe_id": "P30",
        "failure_dimension": "style_guide_adherence",
        "difficulty": "medium",
        "signal_type": "prior_thread",
        "primary_segment": "segment_4_capability_gap",
        "signal_confidence": "medium",
        "ai_score": 2,
        "ai_confidence": "medium",
        "supported_stacks": ["python", "ml", "infra"],
        "pricing_scope": "route_specific_quote_to_human",
        "source_ref": "seed/probe_library.md#P30",
        "source_trace_ids": ["0857ba6e-d8cb-4ec8-b024-3d5ddc298fc6"],
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
        "expected_behavior": "State the demo or fixture boundary plainly before any capability discussion.",
        "failure_rationale": "Demo artifacts presented as live evidence create trust loss.",
        "subject_stems": [
            "Re: artifact provenance",
            "Re: review boundary note",
            "Re: production evidence note",
        ],
        "evidence_templates": [
            "The artifact in question came from a fixture-backed review path rather than a live production run.",
            "The safest phrasing is to keep the review boundary explicit before discussing any production implication.",
            "The production conversation should start only after the fixture-backed artifact is labeled honestly.",
        ],
        "ask_templates": [
            "Can you reply if you want the production-safe review criteria we use before external sharing?",
            "Can you share whether a production checklist would be more useful than another demo artifact?",
            "Can you send the specific artifact question that still needs a production-safe answer?",
        ],
        "prior_thread_templates": [
            "The prospect asked whether a prior artifact reflected a live run or a fixture-backed review path.",
            "The buyer is checking whether the artifact should be treated as production evidence.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "linkedin_dm", "sms"],
        },
        "message_kinds": {
            "train": ["warm_reply", "warm_reply", "reengagement", "warm_reply", "warm_reply", "reengagement"],
            "dev": ["warm_reply", "reengagement", "warm_reply", "warm_reply"],
        },
    },
    {
        "suffix": "competitor-gap-research-frame",
        "probe_id": "P33",
        "failure_dimension": "gap_condescension",
        "difficulty": "hard",
        "signal_type": "competitor_gap",
        "primary_segment": "segment_4_capability_gap",
        "signal_confidence": "high",
        "ai_score": 2,
        "ai_confidence": "high",
        "supported_stacks": ["python", "data", "ml", "infra"],
        "pricing_scope": "public_bands_only",
        "source_ref": "seed/probe_library.md#P33",
        "source_trace_ids": ["a553180f-80d2-4d4b-9a1e-d525b1219cfd"],
        "expected_terms": ["mlops", "manual"],
        "forbidden_terms": ["behind the curve", "you need to", "falling behind"],
        "banned_phrases": ["world-class", "top talent", "quick chat"],
        "tone_markers": ["direct", "grounded", "honest", "professional", "non_condescending"],
        "judge_dimensions": ["gap_condescension", "signal_grounding", "next_step_quality"],
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
        "expected_behavior": "Frame peer-comparison evidence as research rather than buyer deficiency.",
        "failure_rationale": "Competitor-gap evidence becomes risky when it sounds presumptuous or simplistic.",
        "subject_stems": [
            "Question on MLOps scope",
            "Question on workflow coverage",
            "Question on peer automation scope",
        ],
        "evidence_templates": [
            "Peer hiring evidence may reflect a different MLOps operating model rather than a gap to force closed.",
            "The public comparison is useful only if it stays framed as optional workflow research, not a verdict.",
            "A quieter hiring signal can still be a deliberate choice, especially when manual workflow ownership is intentional.",
        ],
        "ask_templates": [
            "Can you reply with one workflow area you prefer to keep manual so the peer comparison stays respectful?",
            "Can you share whether those peer MLOps postings map to work you have intentionally not prioritized?",
            "Can you send one example of where peer automation differs from your preferred workflow design?",
        ],
        "prior_thread_templates": [
            "The buyer asked us to keep the peer comparison practical rather than presumptuous.",
            "The prospect wants evidence framed as research, not as a basic maturity lecture.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "email", "linkedin_dm"],
        },
        "message_kinds": {
            "train": ["cold_outreach", "cold_outreach", "reengagement", "cold_outreach", "cold_outreach", "reengagement"],
            "dev": ["cold_outreach", "reengagement", "cold_outreach", "cold_outreach"],
        },
    },
    {
        "suffix": "timezone-aware-next-step",
        "probe_id": "P34",
        "failure_dimension": "next_step_quality",
        "difficulty": "medium",
        "signal_type": "prior_thread",
        "primary_segment": "segment_3_leadership_transition",
        "signal_confidence": "medium",
        "ai_score": 1,
        "ai_confidence": "medium",
        "supported_stacks": ["python", "data", "ops"],
        "pricing_scope": "public_bands_only",
        "source_ref": "seed/probe_library.md#P34",
        "source_trace_ids": [],
        "expected_terms": ["local", "business hours"],
        "forbidden_terms": ["2 am"],
        "banned_phrases": ["quick chat", "do not miss out"],
        "tone_markers": ["direct", "grounded", "honest", "professional"],
        "judge_dimensions": ["next_step_quality", "signal_grounding", "style_guide_adherence"],
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
        "expected_behavior": "Offer a concrete next step that respects the buyer's local working hours.",
        "failure_rationale": "A careless meeting ask creates friction even when the signal is otherwise valid.",
        "subject_stems": [
            "Re: local-time availability",
            "Re: business-hours alignment",
            "Re: local-hours note",
        ],
        "evidence_templates": [
            "The outreach is more credible when the local time window is treated as a buyer constraint rather than an afterthought.",
            "A grounded follow-up should protect local business hours before it asks for anything more.",
            "The operational signal is strong enough for a practical follow-up, but only if the local-time option stays practical.",
        ],
        "ask_templates": [
            "Can you share one local meeting window that works so we stay inside business hours?",
            "Can you reply with the local time block your team actually uses for vendor meetings?",
            "Can you send the business-hours range that would make a follow-up meeting realistic?",
        ],
        "prior_thread_templates": [
            "The prospect replied that prior scheduling options landed outside local business hours.",
            "The buyer asked for a more practical local-time follow-up option.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "linkedin_dm", "sms"],
        },
        "message_kinds": {
            "train": ["warm_reply", "reengagement", "warm_reply", "warm_reply", "reengagement", "warm_reply"],
            "dev": ["warm_reply", "reengagement", "warm_reply", "warm_reply"],
        },
    },
    {
        "suffix": "output-clean-abstain",
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
        "source_trace_ids": [],
        "expected_terms": ["queue", "workflow"],
        "forbidden_terms": ["clearly"],
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
        "expected_behavior": "Stay well-formed and specific even when the signal is too weak for a strong claim.",
        "failure_rationale": "Thin-signal cases often drift into generic filler instead of a clean, usable abstaining draft.",
        "subject_stems": [
            "Question on queue pressure",
            "Checking the workflow signal",
            "Question on the visible hiring pattern",
        ],
        "evidence_templates": [
            "The visible workflow evidence is still too weak for a strong claim, so the draft should stay precise instead of generic.",
            "A clean abstaining draft can still mention the queue signal without inflating it into certainty.",
            "The safest output is a short workflow note that stays specific about what the public signal cannot prove.",
        ],
        "ask_templates": [
            "Can you reply with one queue example if the outside workflow signal is incomplete?",
            "Can you share one workflow bottleneck if the public signal is missing the real issue?",
            "Can you send one example that would make the queue signal more concrete?",
        ],
        "prior_thread_templates": [
            "The buyer asked for a shorter follow-up that stays specific instead of generic.",
            "The prospect confirmed SMS follow-up is okay if the note stays concrete and restrained.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "linkedin_dm", "sms"],
        },
        "message_kinds": {
            "train": ["cold_outreach", "reengagement", "cold_outreach", "cold_outreach", "reengagement", "cold_outreach"],
            "dev": ["cold_outreach", "reengagement", "cold_outreach", "warm_reply"],
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


def sentence_for(options: list[str], index: int) -> str:
    return options[index % len(options)]


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
        body = f"{greeting}{intro} {ask}"
        return {"body": body}
    if channel == "linkedin_dm":
        body = f"{greeting}{intro} {ask}"
        return {"body": body}

    prefix = "Re: " if message_kind != "cold_outreach" else ""
    subject = f"{prefix}{sentence_for(blueprint['subject_stems'], index)}"
    body = f"{greeting}{intro} {ask}"
    return {"subject": subject[:60], "body": body}


def max_body_words_for(message_kind: str) -> int:
    if message_kind == "cold_outreach":
        return 120
    if message_kind == "reengagement":
        return 100
    return 200


def materialize_tasks(partition: str) -> list[dict[str, Any]]:
    held_out_ids = load_held_out_trace_ids()
    tasks: list[dict[str, Any]] = []
    for blueprint_index, blueprint in enumerate(PROGRAMMATIC_BLUEPRINTS, start=1):
        channels = blueprint["channels"][partition]
        message_kinds = blueprint["message_kinds"][partition]
        if len(channels) != len(message_kinds):
            raise ValueError(f"Channel/message plan mismatch for {blueprint['suffix']} {partition}.")
        for variant_index, channel in enumerate(channels):
            message_kind = message_kinds[variant_index]
            prospect = PROSPECTS[(blueprint_index * 3 + variant_index) % len(PROSPECTS)]
            task_index = len(tasks) + 1
            candidate_output = candidate_output_for(
                blueprint,
                prospect,
                channel,
                message_kind,
                variant_index,
            )
            task = {
                "task_id": f"{partition}-programmatic-{task_index:03d}-{blueprint['suffix']}",
                "partition": partition,
                "source_mode": "programmatic",
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
                    "source_artifact": blueprint["source_ref"].split("#", maxsplit=1)[0],
                    "style_guide_version": "v2",
                    **(
                        {"source_trace_ids": blueprint["source_trace_ids"]}
                        if blueprint["source_trace_ids"]
                        else {}
                    ),
                },
            }
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
