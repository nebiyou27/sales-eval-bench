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
    # ── Wave 2 blueprints ──────────────────────────────────────────────────────
    {
        "suffix": "pricing-scope-boundary",
        "probe_id": "P26",
        "failure_dimension": "signal_grounding",
        "difficulty": "hard",
        "signal_type": "pricing_scope",
        "primary_segment": "segment_1_recently_funded",
        "signal_confidence": "medium",
        "ai_score": 2,
        "ai_confidence": "medium",
        "supported_stacks": ["python", "data", "ops"],
        "pricing_scope": "route_specific_quote_to_human",
        "source_ref": "seed/probe_library.md#P26",
        "source_trace_ids": [],
        "expected_terms": ["pricing", "scope"],
        "forbidden_terms": ["all-in", "custom rate"],
        "banned_phrases": ["world-class", "quick chat", "synergize"],
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
        "expected_behavior": "Stay within public_bands_only pricing scope and route any rate enquiry to a human reviewer.",
        "failure_rationale": "Implying a rate commitment beyond the visible scope creates delivery and trust risk.",
        "subject_stems": [
            "Question on pricing scope",
            "Note on rate scope",
            "Question on scope boundary",
        ],
        "evidence_templates": [
            "The workflow signal here only supports a public_bands_only pricing scope, so any route-specific rate conversation needs a human reviewer first.",
            "The sales engagement stays within the pricing scope that is visible here, not a broader rate commitment that has not been verified.",
            "Keeping the pricing scope explicit means the conversation stays grounded in what the public signal can actually support.",
        ],
        "ask_templates": [
            "Can you reply with one pricing question that still fits within the public scope?",
            "Can you share the one rate constraint that would need a human reviewer before we proceed?",
            "Can you send one example where the scope needs to be confirmed before any rate discussion?",
        ],
        "prior_thread_templates": [
            "The prospect asked whether the rate discussion should go through a formal pricing review.",
            "The buyer confirmed the scope should stay within the public pricing band for now.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "linkedin_dm", "email"],
        },
        "message_kinds": {
            "train": ["cold_outreach", "cold_outreach", "warm_reply", "reengagement", "cold_outreach", "warm_reply"],
            "dev": ["cold_outreach", "warm_reply", "cold_outreach", "reengagement"],
        },
    },
    {
        "suffix": "capacity-gate-first",
        "probe_id": "P31",
        "failure_dimension": "next_step_quality",
        "difficulty": "hard",
        "signal_type": "bench_match",
        "primary_segment": "segment_4_capability_gap",
        "signal_confidence": "medium",
        "ai_score": 2,
        "ai_confidence": "medium",
        "supported_stacks": ["python", "backend", "ops"],
        "pricing_scope": "route_specific_quote_to_human",
        "source_ref": "seed/probe_library.md#P31",
        "source_trace_ids": [],
        "expected_terms": ["capacity", "gate"],
        "forbidden_terms": ["fully committed", "guaranteed capacity"],
        "banned_phrases": ["world-class", "quick chat", "do not miss out"],
        "tone_markers": ["direct", "grounded", "honest", "professional"],
        "judge_dimensions": ["next_step_quality", "signal_grounding", "style_guide_adherence"],
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
        "expected_behavior": "Clear the capacity gate before offering any delivery timeline or commitment.",
        "failure_rationale": "Skipping the capacity gate creates premature commitments that erode buyer trust.",
        "subject_stems": [
            "Question on capacity gate",
            "Note on delivery gate",
            "Question on gate requirements",
        ],
        "evidence_templates": [
            "The capacity gate has to stay open before any delivery commitment can be confirmed.",
            "Skipping the capacity gate means any next-step commitment would be premature given the current capacity state.",
            "A capacity review is the gate that needs to clear before a delivery timeline becomes realistic.",
        ],
        "ask_templates": [
            "Can you share the one capacity question that still needs to clear before we discuss delivery?",
            "Can you reply with the gate criteria that would let us move to a timeline conversation?",
            "Can you send one example of a capacity concern that still needs to be addressed?",
        ],
        "prior_thread_templates": [
            "The prospect asked whether the delivery timeline depends on a capacity review first.",
            "The buyer wants to confirm the capacity gate before any commitments are made.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "linkedin_dm", "email"],
        },
        "message_kinds": {
            "train": ["warm_reply", "warm_reply", "cold_outreach", "reengagement", "warm_reply", "reengagement"],
            "dev": ["warm_reply", "reengagement", "warm_reply", "cold_outreach"],
        },
    },
    {
        "suffix": "leadership-gap-frame",
        "probe_id": "P33",
        "failure_dimension": "gap_condescension",
        "difficulty": "medium",
        "signal_type": "leadership_change",
        "primary_segment": "segment_3_leadership_transition",
        "signal_confidence": "medium",
        "ai_score": 1,
        "ai_confidence": "medium",
        "supported_stacks": ["python", "data", "ops"],
        "pricing_scope": "public_bands_only",
        "source_ref": "seed/probe_library.md#P33",
        "source_trace_ids": [],
        "expected_terms": ["transition", "workflow"],
        "forbidden_terms": ["you need to", "falling behind", "behind the curve"],
        "banned_phrases": ["world-class", "quick chat", "top talent"],
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
        "expected_behavior": "Frame leadership-transition evidence as a workflow research question rather than a gap verdict.",
        "failure_rationale": "Asserting a gap based on a leadership change presumes the new team has not already addressed it.",
        "subject_stems": [
            "Question on transition workflow",
            "Note on leadership workflow scope",
            "Question on workflow after transition",
        ],
        "evidence_templates": [
            "A leadership transition can create workflow gaps, but the signal is too ambiguous to assume the team needs external tooling.",
            "The visible transition signal suggests a workflow adjustment period rather than a persistent capability gap.",
            "Leadership transitions often come with workflow resets that the team handles internally before external help is relevant.",
        ],
        "ask_templates": [
            "Can you share what workflow area changed most after the leadership transition?",
            "Can you reply with one workflow question the team is still figuring out after the change?",
            "Can you send one example where the workflow reset has stalled since the transition?",
        ],
        "prior_thread_templates": [
            "The buyer asked us to keep the transition framing research-oriented rather than presumptuous.",
            "The prospect wants the leadership signal treated as an open question, not a confirmed gap.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "linkedin_dm", "email"],
        },
        "message_kinds": {
            "train": ["cold_outreach", "cold_outreach", "warm_reply", "cold_outreach", "cold_outreach", "reengagement"],
            "dev": ["cold_outreach", "warm_reply", "cold_outreach", "reengagement"],
        },
    },
    {
        "suffix": "maturity-score-conservative",
        "probe_id": "P25",
        "failure_dimension": "ai_maturity_consistency",
        "difficulty": "easy",
        "signal_type": "ai_maturity",
        "primary_segment": "segment_4_capability_gap",
        "signal_confidence": "low",
        "ai_score": 1,
        "ai_confidence": "low",
        "supported_stacks": ["python", "data"],
        "pricing_scope": "public_bands_only",
        "source_ref": "seed/probe_library.md#P25",
        "source_trace_ids": [],
        "expected_terms": ["maturity", "workflow"],
        "forbidden_terms": ["certainly", "definitively"],
        "banned_phrases": ["world-class", "i hope this email finds you well", "quick chat"],
        "tone_markers": ["direct", "grounded", "honest", "professional"],
        "judge_dimensions": ["ai_maturity_consistency", "signal_grounding", "output_validity"],
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
        "expected_behavior": "Stay exploratory and low-confidence when the maturity score is 1 with low confidence.",
        "failure_rationale": "Asserting capability claims at a low maturity score overstates the visible evidence.",
        "subject_stems": [
            "Question on maturity read",
            "Note on workflow maturity",
            "Question on maturity confidence",
        ],
        "evidence_templates": [
            "The maturity signal here stays at score 1 with low confidence, so the workflow framing should stay exploratory rather than assertive.",
            "A low-confidence maturity read means the workflow diagnosis should start with a question rather than a capability claim.",
            "The AI maturity signal is too uncertain to support a strong workflow claim without more evidence from the buyer.",
        ],
        "ask_templates": [
            "Can you share one workflow example that would help validate the maturity read?",
            "Can you reply with one automation area where your team is still exploring options?",
            "Can you send one workflow question that is still open at the current maturity level?",
        ],
        "prior_thread_templates": [
            "The prospect asked for a more honest framing of the AI maturity assessment.",
            "The buyer wants the maturity read to stay exploratory given the low confidence level.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "email", "linkedin_dm"],
        },
        "message_kinds": {
            "train": ["cold_outreach", "warm_reply", "warm_reply", "reengagement", "cold_outreach", "warm_reply"],
            "dev": ["cold_outreach", "warm_reply", "reengagement", "cold_outreach"],
        },
    },
    {
        "suffix": "reengagement-format-check",
        "probe_id": "P29",
        "failure_dimension": "output_validity",
        "difficulty": "medium",
        "signal_type": "prior_thread",
        "primary_segment": "segment_2_restructuring_cost",
        "signal_confidence": "low",
        "ai_score": 1,
        "ai_confidence": "medium",
        "supported_stacks": ["python", "data"],
        "pricing_scope": "public_bands_only",
        "source_ref": "seed/probe_library.md#P29",
        "source_trace_ids": [],
        "expected_terms": ["workflow", "queue"],
        "forbidden_terms": ["obviously", "clearly"],
        "banned_phrases": ["world-class", "quick question", "do not miss out"],
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
        "expected_behavior": "Keep the reengagement well-formed and specific to the visible queue signal rather than generic.",
        "failure_rationale": "Thin-signal reengagements often drift into generic filler that loses the workflow grounding.",
        "subject_stems": [
            "Re: workflow follow-up",
            "Re: queue signal check",
            "Re: workflow reengagement",
        ],
        "evidence_templates": [
            "A well-formed reengagement should stay specific about the workflow bottleneck rather than drift into generic prose.",
            "The signal is still too weak for a confident assertion, so the reengagement must stay grounded in the visible queue evidence.",
            "The reengagement format stays valid by keeping the workflow reference concrete and the ask specific.",
        ],
        "ask_templates": [
            "Can you send one queue example if the outside signal is missing something material?",
            "Can you reply with one workflow case that would make the reengagement more specific?",
            "Can you share one queue bottleneck that would sharpen the reengagement framing?",
        ],
        "prior_thread_templates": [
            "The buyer asked for a more specific reengagement that stays tied to the workflow signal.",
            "The prospect confirmed the reengagement should stay grounded rather than generic.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "linkedin_dm", "email"],
        },
        "message_kinds": {
            "train": ["reengagement", "reengagement", "warm_reply", "reengagement", "reengagement", "warm_reply"],
            "dev": ["reengagement", "warm_reply", "reengagement", "warm_reply"],
        },
    },
    {
        "suffix": "style-prefix-explicit",
        "probe_id": "P30",
        "failure_dimension": "style_guide_adherence",
        "difficulty": "easy",
        "signal_type": "prior_thread",
        "primary_segment": "segment_4_capability_gap",
        "signal_confidence": "low",
        "ai_score": 1,
        "ai_confidence": "low",
        "supported_stacks": ["python", "infra"],
        "pricing_scope": "public_bands_only",
        "source_ref": "seed/probe_library.md#P30",
        "source_trace_ids": [],
        "expected_terms": ["scope", "review"],
        "forbidden_terms": ["production-ready", "live run"],
        "banned_phrases": ["quick chat", "do not miss out", "world-class"],
        "tone_markers": ["direct", "grounded", "honest", "professional"],
        "judge_dimensions": ["style_guide_adherence", "signal_grounding", "next_step_quality"],
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
        "expected_behavior": "Label the review scope and fixture boundary explicitly before any capability discussion.",
        "failure_rationale": "Unlabeled review scope lets fixture artifacts be misread as production evidence.",
        "subject_stems": [
            "Re: review scope note",
            "Re: scope boundary note",
            "Re: fixture review scope",
        ],
        "evidence_templates": [
            "The review scope should stay explicit so the buyer knows which artifacts are fixture-backed before the conversation advances.",
            "Keeping the scope of the review labeled prevents any artifact from being misread as production evidence.",
            "The fixture scope needs to be named before the review conversation can move to production implications.",
        ],
        "ask_templates": [
            "Can you reply with one review question that still needs a scope clarification?",
            "Can you share which artifact from the review still needs an explicit scope label?",
            "Can you send one example where the scope was unclear during the review?",
        ],
        "prior_thread_templates": [
            "The prospect asked whether the earlier artifact represented a fixture-backed review scope or production evidence.",
            "The buyer wants the review scope labeled explicitly before the conversation advances.",
        ],
        "channels": {
            "train": ["email", "email", "email", "email", "linkedin_dm", "linkedin_dm"],
            "dev": ["email", "email", "email", "linkedin_dm", "email", "linkedin_dm", "email"],
        },
        "message_kinds": {
            "train": ["warm_reply", "warm_reply", "reengagement", "warm_reply", "warm_reply", "reengagement"],
            "dev": ["warm_reply", "reengagement", "warm_reply", "warm_reply", "warm_reply", "reengagement", "reengagement"],
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
