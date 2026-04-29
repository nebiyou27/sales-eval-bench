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
    # ── Wave 3 hard seeds (train) ─────────────────────────────────────────────
    {
        "partition": "train",
        "suffix": "gap-condescension-ex-ml-lead",
        "difficulty": "hard",
        "failure_dimension": "gap_condescension",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Vector Systems",
                "contact_role": "VP ML Engineering",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "competitor_gap",
                        "evidence": "Peer firms added MLOps roles in the last quarter, but the prospect is an ex-Google ML lead who likely designed the monitoring stack intentionally.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P33",
                    }
                ],
                "ai_maturity": {"score": 3, "confidence": "high"},
            },
            "bench_context": {
                "supported_stacks": ["python", "ml", "infra"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {"contacted_before": False, "summary": ""},
        },
        "candidate_output": {
            "subject": "Question on MLOps workflow at Vector Systems",
            "body": (
                "Hi Priya, Peer firms staffed MLOps roles last quarter, but that pattern may reflect a different workflow model rather than a gap in yours. "
                "Can you share one workflow area where outside support would actually add more than your current stack?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Frame peer evidence as optional research; do not assume a gap for a senior ML practitioner.",
            "target_decision": "accept",
            "failure_rationale": "Gap language directed at an expert buyer presumes incompetence and destroys trust immediately.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional", "non_condescending"],
            "expected_terms": ["mlops", "workflow"],
            "forbidden_terms": ["behind the curve", "you need to", "basic"],
            "banned_phrases": ["world-class", "quick chat", "top talent"],
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
            "authoring_note": "Hard seed: ex-Google ML lead; gap language is maximally risky and must be avoided.",
        },
    },
    {
        "partition": "train",
        "suffix": "ai-maturity-conflicting-signals",
        "difficulty": "hard",
        "failure_dimension": "ai_maturity_consistency",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Driftwell Data",
                "contact_role": "VP Analytics",
                "company_stage": "series_b",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "ai_maturity",
                        "evidence": "One public signal shows active ML infra hiring (suggests score 2), but a separate hiring freeze notice suggests the team may be contracting rather than expanding.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P24",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "ml"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "route_specific_quote_to_human",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The buyer asked how we arrived at the maturity read given the contradictory hiring signals.",
            },
        },
        "candidate_output": {
            "subject": "Re: maturity read with conflicting signals",
            "body": (
                "Hi Leah, I should be upfront: the two hiring signals point in opposite directions, so I have kept the maturity read at score 1 with low confidence rather than averaging them into a false middle. "
                "Can you reply with which signal better reflects the actual workflow state today?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "When signals conflict, degrade to the lower confidence estimate and name the conflict explicitly.",
            "target_decision": "accept",
            "failure_rationale": "Averaging conflicting signals into a confident maturity claim is worse than acknowledging the contradiction.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["workflow", "signals"],
            "forbidden_terms": ["obviously", "just need to"],
            "banned_phrases": ["world-class", "i hope this email finds you well", "quick chat"],
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
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hard seed: two conflicting maturity signals; conservative degradation is required.",
        },
    },
    {
        "partition": "train",
        "suffix": "ai-maturity-score-3-restraint",
        "difficulty": "hard",
        "failure_dimension": "ai_maturity_consistency",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "ArcLight AI",
                "contact_role": "CTO",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "high",
                "signals": [
                    {
                        "signal_type": "ai_maturity",
                        "evidence": "The prospect self-describes their ML platform as fully productionised with dedicated MLOps infrastructure, suggesting score 3.",
                        "confidence": "high",
                        "source_ref": "seed/probe_library.md#P25",
                    }
                ],
                "ai_maturity": {"score": 3, "confidence": "high"},
            },
            "bench_context": {
                "supported_stacks": ["python", "ml", "infra"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "route_specific_quote_to_human",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The buyer confirmed their ML stack is fully productionised and asked how Tenacious adds value at this maturity level.",
            },
        },
        "candidate_output": {
            "subject": "Re: value at high ML maturity",
            "body": (
                "Hi Sam, At score 3 the workflow gaps are usually narrow and specific rather than broad, so I would rather not assume one rather than name the right area. "
                "Can you share one workflow step where external support would complement rather than replace your existing ML infrastructure?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "At maximum maturity score, avoid broad capability claims and ask about narrow specific gaps instead.",
            "target_decision": "accept",
            "failure_rationale": "Recommending broad tooling to a high-maturity buyer sounds uninformed and condescending.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["workflow", "ml"],
            "forbidden_terms": ["obviously", "just need to"],
            "banned_phrases": ["world-class", "quick chat", "industry-leading"],
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
            "probe_id": "P25",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hard seed: max maturity score requires narrow, specific framing — broad claims would be presumptuous.",
        },
    },
    {
        "partition": "train",
        "suffix": "signal-grounding-zero-evidence",
        "difficulty": "hard",
        "failure_dimension": "signal_grounding",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Onyx Systems",
                "contact_role": "Head of Engineering",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "job_post_velocity",
                        "evidence": "No credible public hiring signal is visible for this account; the segment classification rests on company size alone.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P29",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {"contacted_before": False, "summary": ""},
        },
        "candidate_output": {
            "subject": "Question on workflow pressure at Onyx",
            "body": (
                "Hi Jordan, I cannot point to a specific public signal at Onyx right now, so I would rather ask than assume. "
                "Can you share one workflow area where capacity has become a constraint this quarter?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "When no credible signal exists, abstain from any capability claim and ask openly instead.",
            "target_decision": "accept",
            "failure_rationale": "Claiming a workflow gap with zero evidence is fabrication regardless of segment classification.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["workflow"],
            "forbidden_terms": ["your peers", "falling behind", "clearly"],
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
            "probe_id": "P29",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hard seed: zero public evidence; any gap claim is fabrication and must be abstained.",
        },
    },
    {
        "partition": "train",
        "suffix": "signal-grounding-stale-funding",
        "difficulty": "hard",
        "failure_dimension": "signal_grounding",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Ridgecrest Labs",
                "contact_role": "VP Engineering",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_1_recently_funded",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "funding_event",
                        "evidence": "A Series B funding announcement is visible but dated 22 months ago; the claim is below the 18-month freshness threshold and should not anchor the outreach.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P07",
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
            "subject": "Question on workflow capacity at Ridgecrest",
            "body": (
                "Hi Kim, I am not going to anchor this on the old funding announcement since the signal is past the freshness window. "
                "Can you share what the workflow capacity picture looks like today rather than when the round closed?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Discard stale funding evidence explicitly and ask for current state instead.",
            "target_decision": "accept",
            "failure_rationale": "Using a 22-month-old funding claim as a growth signal is a misclassification risk (P07).",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["workflow"],
            "forbidden_terms": ["your recent funding", "just raised"],
            "banned_phrases": ["quick chat", "world-class", "exciting times"],
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
            "probe_id": "P07",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hard seed: stale funding signal must be explicitly discarded, not used as outreach anchor.",
        },
    },
    {
        "partition": "train",
        "suffix": "next-step-timezone-hard",
        "difficulty": "hard",
        "failure_dimension": "next_step_quality",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Helix East",
                "contact_role": "CTO",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_3_leadership_transition",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "The prospect is based in Addis Ababa (UTC+3); prior scheduling attempts proposed slots at 2 AM local time, which the buyer noted was not viable.",
                        "confidence": "high",
                        "source_ref": "seed/probe_library.md#P34",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "ops"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The buyer replied that the proposed slots were in the middle of the night local time and asked for options that respect local business hours.",
            },
        },
        "candidate_output": {
            "subject": "Re: local business hours follow-up",
            "body": (
                "Hi Felix, I should have checked the local time before proposing those slots. "
                "Can you reply with a local business hours window in Addis Ababa that would work for a follow-up?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Acknowledge the timezone error and propose a local-hours-aware next step.",
            "target_decision": "accept",
            "failure_rationale": "Repeating a 2 AM scheduling ask after the buyer flagged it signals carelessness and disrespect.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["local", "business hours"],
            "forbidden_terms": ["2 am", "early morning"],
            "banned_phrases": ["quick chat", "world-class", "do not miss out"],
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
                "banned_condescension_absent",
                "expected_signal_term_present",
                "forbidden_terms_absent",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ],
            "judge_dimensions": ["next_step_quality", "signal_grounding", "style_guide_adherence"],
        },
        "metadata": {
            "probe_id": "P34",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hard seed: prior 2 AM slot failure; local-business-hours recovery ask is required.",
        },
    },
    {
        "partition": "train",
        "suffix": "next-step-premature-commit",
        "difficulty": "hard",
        "failure_dimension": "next_step_quality",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Juniper Lake",
                "contact_role": "VP Revenue Systems",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "bench_match",
                        "evidence": "The buyer asked for a delivery timeline, but the capacity gate has not cleared and backend capacity for this scope has not been verified.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P31",
                    }
                ],
                "ai_maturity": {"score": 2, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "ops"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "route_specific_quote_to_human",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prospect asked for a concrete delivery timeline before the capacity review has taken place.",
            },
        },
        "candidate_output": {
            "subject": "Re: delivery timeline gate",
            "body": (
                "Hi Mina, I want to give you a reliable timeline rather than one that changes after the capacity review. "
                "Can you share the delivery scope so we can clear the gate before I commit to dates?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Gate the timeline commitment behind the capacity review; do not give a number that will need to be walked back.",
            "target_decision": "accept",
            "failure_rationale": "Committing to a timeline before capacity is verified creates trust-eroding scope changes later.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["capacity", "gate"],
            "forbidden_terms": ["guaranteed", "fully committed"],
            "banned_phrases": ["world-class", "quick chat", "no problem at all"],
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
                "banned_condescension_absent",
                "expected_signal_term_present",
                "forbidden_terms_absent",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ],
            "judge_dimensions": ["next_step_quality", "signal_grounding", "style_guide_adherence"],
        },
        "metadata": {
            "probe_id": "P31",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hard seed: buyer asks for timeline before capacity gate clears; gating is the correct response.",
        },
    },
    {
        "partition": "train",
        "suffix": "output-validity-sms-word-limit",
        "difficulty": "hard",
        "failure_dimension": "output_validity",
        "channel": "sms",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "SkyBridge Tech",
                "contact_role": "VP Operations",
                "company_stage": "series_b",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_2_restructuring_cost",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "The prospect confirmed SMS follow-up is acceptable after the prior email exchange; the output must respect the warm-reply SMS word limit.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P12",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "ops", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prospect explicitly confirmed SMS follow-up is okay after the earlier email thread about restructuring capacity.",
            },
        },
        "candidate_output": {
            "body": (
                "Hi Chris, The restructuring signal from the prior thread is still worth exploring. "
                "Can you share one operational area where staffing pressure is highest right now?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Produce a valid warm-reply SMS within the 100-word reengagement limit, grounded in the prior thread.",
            "target_decision": "accept",
            "failure_rationale": "An SMS output that exceeds the reengagement word limit or omits the prior-thread reference fails output validity.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["restructuring", "operational"],
            "forbidden_terms": ["obviously", "clearly"],
            "banned_phrases": ["world-class", "quick chat", "do not miss out"],
            "max_body_words": 100,
            "one_ask_required": True,
            "require_signal_reference": True,
            "confidence_aware_language": True,
            "forbid_bench_term": True,
            "allowed_channels": ["sms"],
        },
        "scoring_config": {
            "deterministic_dimensions": [
                "output_nonempty",
                "max_body_words_respected",
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
            "probe_id": "P12",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hard seed: warm SMS reengagement must stay within 100-word limit and reference the prior thread.",
        },
    },
    {
        "partition": "train",
        "suffix": "style-guide-demo-as-production",
        "difficulty": "hard",
        "failure_dimension": "style_guide_adherence",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Blue Current Analytics",
                "contact_role": "Head of Revenue Ops",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "The reviewer found that an artifact shared in the prior thread was labeled as a production output but came from a test mode run.",
                        "confidence": "high",
                        "source_ref": "seed/probe_library.md#P30",
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
                "summary": "The prospect flagged that the artifact from the prior session appears to come from a demo pipeline rather than a production run.",
            },
        },
        "candidate_output": {
            "subject": "Re: artifact provenance correction",
            "body": (
                "Hi Avery, That artifact came from a test mode run, not a production workflow. "
                "I should have labeled that clearly before sharing it. "
                "Can you share which part of the output you want replicated with a production-safe version?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Acknowledge the demo-mode provenance immediately and offer a production-safe replacement.",
            "target_decision": "accept",
            "failure_rationale": "Letting a demo artifact be treated as production evidence without correction destroys reviewer trust.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["production", "demo"],
            "forbidden_terms": ["production-ready", "live run"],
            "banned_phrases": ["quick chat", "world-class", "do not miss out"],
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
                "banned_condescension_absent",
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
            "authoring_note": "Hard seed: demo artifact mislabeled as production; explicit correction is required.",
        },
    },
    {
        "partition": "train",
        "suffix": "ai-maturity-fabricated-benchmark",
        "difficulty": "hard",
        "failure_dimension": "ai_maturity_consistency",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "PinePath Analytics",
                "contact_role": "VP Data",
                "company_stage": "series_b",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "ai_maturity",
                        "evidence": "The buyer asked where the AI maturity score came from and whether it references a public benchmark URL.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P26",
                    }
                ],
                "ai_maturity": {"score": 2, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "route_specific_quote_to_human",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prospect asked whether the maturity read references a third-party benchmark or only signals from the current thread.",
            },
        },
        "candidate_output": {
            "subject": "Re: source for the maturity score",
            "body": (
                "Hi Omar, The maturity score comes from the CRM and workflow signals already in our thread, not from an external benchmark URL I have not named. "
                "Can you share one workflow example that would let me validate the score against something concrete?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Name only sources actually used; do not invent a benchmark URL to make the maturity read sound more authoritative.",
            "target_decision": "accept",
            "failure_rationale": "Fabricating a benchmark URL (P26) makes the maturity reasoning look stronger than the evidence supports.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["crm", "workflow"],
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
            "authoring_note": "Hard seed: buyer explicitly asks for benchmark URL; fabricating one is the failure mode to prevent.",
        },
    },
    {
        "partition": "train",
        "suffix": "gap-condescension-warm-reply-hard",
        "difficulty": "hard",
        "failure_dimension": "gap_condescension",
        "channel": "email",
        "message_kind": "reengagement",
        "input": {
            "prospect": {
                "company_name": "Crestwater Engineering",
                "contact_role": "VP Engineering",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "competitor_gap",
                        "evidence": "Peer engineering teams added MLOps capacity, but reengaging with gap framing after a prior non-reply would amplify condescension risk.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P33",
                    }
                ],
                "ai_maturity": {"score": 2, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "ml", "infra"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prior outreach received no reply; the temptation is to escalate with a stronger gap claim to prompt engagement.",
            },
        },
        "candidate_output": {
            "subject": "Re: workflow question from earlier",
            "body": (
                "Hi Morgan, I am following up on the earlier workflow question without escalating the framing. "
                "Can you share one workflow area where outside capacity would genuinely help, if the timing is better now?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Reengage without escalating gap language; a non-reply does not warrant stronger condescension.",
            "target_decision": "accept",
            "failure_rationale": "Escalating gap claims after a non-reply pressures the buyer and amplifies condescension risk.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional", "non_condescending"],
            "expected_terms": ["workflow"],
            "forbidden_terms": ["behind the curve", "you need to", "falling behind"],
            "banned_phrases": ["world-class", "quick chat", "last chance"],
            "max_body_words": 100,
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
            "authoring_note": "Hard seed: reengagement after non-reply; gap escalation is the failure mode to prevent.",
        },
    },
    {
        "partition": "train",
        "suffix": "gap-condescension-linkedin-hard",
        "difficulty": "hard",
        "failure_dimension": "gap_condescension",
        "channel": "linkedin_dm",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Flare Data",
                "contact_role": "Head of Data Engineering",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "competitor_gap",
                        "evidence": "Peer firms in the same vertical hired ML engineers, but DM context makes gap language harder to correct and more damaging to relationship.",
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
            "body": (
                "Hi Taylor, Peer firms in your vertical have been adding ML data engineering roles recently, though that pattern may reflect a different workflow model than yours. "
                "Can you share whether that shift is relevant to how your team is structured today?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Frame peer hiring as a research observation, not a gap verdict, especially in a first-touch LinkedIn DM.",
            "target_decision": "accept",
            "failure_rationale": "Gap language in a first-touch DM is irreversible and destroys any chance of a relationship.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional", "non_condescending"],
            "expected_terms": ["workflow", "ml"],
            "forbidden_terms": ["behind the curve", "you need to", "falling behind"],
            "banned_phrases": ["world-class", "quick chat", "top talent"],
            "max_body_words": 120,
            "max_subject_chars": 60,
            "one_ask_required": True,
            "require_signal_reference": True,
            "confidence_aware_language": True,
            "forbid_bench_term": True,
            "allowed_channels": ["linkedin_dm"],
        },
        "scoring_config": {
            "deterministic_dimensions": [
                "output_nonempty",
                "max_body_words_respected",
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
            "authoring_note": "Hard seed: LinkedIn DM cold outreach; gap language is irreversible in this channel.",
        },
    },
    {
        "partition": "train",
        "suffix": "signal-grounding-ambiguous-layoff",
        "difficulty": "hard",
        "failure_dimension": "signal_grounding",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Clearstream Analytics",
                "contact_role": "VP Operations",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_2_restructuring_cost",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "layoff_event",
                        "evidence": "A layoff notice is present in the public record but the headcount number is blank; the evidence matches P09/P10 and the claim should not be emitted.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P10",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "ops"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {"contacted_before": False, "summary": ""},
        },
        "candidate_output": {
            "subject": "Question on operational capacity at Clearstream",
            "body": (
                "Hi Dana, I can see a restructuring notice in the public record but the headcount detail is missing, so I am not going to claim a specific capacity picture. "
                "Can you share one workflow area where capacity has tightened so I can stay grounded in what is actually true?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Abstain from a layoff-magnitude claim when the headcount number is blank; ask for a concrete workflow example instead.",
            "target_decision": "accept",
            "failure_rationale": "Inventing a headcount magnitude from a blank-count layoff record damages trust and classification accuracy.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["workflow", "capacity"],
            "forbidden_terms": ["laid off", "cut headcount"],
            "banned_phrases": ["quick chat", "world-class", "exciting times"],
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
            "judge_dimensions": ["signal_grounding", "output_validity", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P10",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hard seed: blank-count layoff signal; inventing headcount magnitude is the failure mode.",
        },
    },
    {
        "partition": "train",
        "suffix": "multi-thread-account-consistency",
        "difficulty": "hard",
        "failure_dimension": "signal_grounding",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Riverglass Capital",
                "contact_role": "CFO",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_2_restructuring_cost",
                "signal_confidence": "high",
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "A parallel thread with the CTO framed the company as Segment 2 restructuring; this CFO thread must use the same framing to avoid account-level inconsistency (P35).",
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
                "summary": "The CTO is in a separate thread discussing post-restructuring delivery capacity; this CFO thread must stay consistent with that framing.",
            },
        },
        "candidate_output": {
            "subject": "Re: keeping account framing consistent",
            "body": (
                "Hi Owen, I want to keep the framing consistent with what your CTO and I discussed: the signal is post-restructuring delivery capacity, not a generic growth or capability-gap pitch. "
                "Can you share whether the finance view of that capacity picture matches the engineering framing?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Maintain the same segment framing across all contacts at the same account.",
            "target_decision": "accept",
            "failure_rationale": "Telling the CFO a different story than the CTO creates account-level inconsistency and destroys trust.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["consistent", "capacity"],
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
                "banned_condescension_absent",
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
            "authoring_note": "Hard seed: parallel CFO/CTO threads; account-level framing consistency is the requirement.",
        },
    },
    {
        "partition": "train",
        "suffix": "gap-condescension-pricing-signal",
        "difficulty": "hard",
        "failure_dimension": "gap_condescension",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Ironclad Ops",
                "contact_role": "COO",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_2_restructuring_cost",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "pricing_scope",
                        "evidence": "The visible pricing evidence suggests cost pressure, but framing cost pressure as a gap the COO has failed to solve is condescending.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P33",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "ops"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {"contacted_before": False, "summary": ""},
        },
        "candidate_output": {
            "subject": "Question on operational cost framing",
            "body": (
                "Hi Rafael, The public pricing signal suggests cost pressure is a factor, but that context may reflect a deliberate ops decision rather than a gap. "
                "Can you share whether the cost picture is something the team is actively working through?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Frame cost pressure as a context question rather than a gap the COO has failed to address.",
            "target_decision": "accept",
            "failure_rationale": "Implying a COO has missed an obvious cost fix is condescending and closes the conversation.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional", "non_condescending"],
            "expected_terms": ["cost", "ops"],
            "forbidden_terms": ["behind the curve", "you need to", "obviously"],
            "banned_phrases": ["world-class", "quick chat", "top talent"],
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
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Hard seed: cost-pressure signal to COO; framing as a gap the COO failed to fix is condescending.",
        },
    },
    # ── Additional held_out hard seeds ──────────────────────────────────────
    {
        "partition": "held_out",
        "suffix": "unverified-citation-retraction",
        "difficulty": "hard",
        "failure_dimension": "signal_grounding",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Prism Systems",
                "contact_role": "Head of Data Science",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_1_recently_funded",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "job_post_velocity",
                        "evidence": "A headcount projection was included in a prior note based on a press paraphrase rather than a verified source filing.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P03",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The buyer asked where the headcount projection came from; the source was a press blurb, not a documented public filing.",
            },
        },
        "candidate_output": {
            "subject": "Re: headcount estimate retraction",
            "body": (
                "Hi Patricia, The headcount projection in my earlier note came from a press paraphrase rather than a verified public filing, and I should retract it rather than let it stand as a documented fact. "
                "Can you share what the actual engineering team picture looks like so I can ground my next note accurately?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Retract a paraphrase-sourced headcount claim and replace it with a direct question about actual state.",
            "target_decision": "accept",
            "failure_rationale": "Presenting a press paraphrase as a verified claim is a citation integrity failure that undermines trust.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["headcount", "engineering"],
            "forbidden_terms": ["confirmed figure", "documented headcount"],
            "banned_phrases": ["world-class", "quick chat", "exciting times"],
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
                "banned_condescension_absent",
                "expected_signal_term_present",
                "forbidden_terms_absent",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ],
            "judge_dimensions": ["signal_grounding", "style_guide_adherence", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P03",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out hard seed: paraphrase-sourced claim retraction; P03 citation-coverage failure.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "duplicate-send-acknowledgment",
        "difficulty": "hard",
        "failure_dimension": "next_step_quality",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Vantage Revenue",
                "contact_role": "Head of Revenue Operations",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_2_restructuring_cost",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "A provider delivery error caused the same outreach message to arrive twice at the same inbox; the buyer replied querying why two identical notes arrived.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P19",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "revops"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "A provider delivery error caused the note to reach the inbox twice; the buyer replied asking why.",
            },
        },
        "candidate_output": {
            "subject": "Re: duplicate message apology",
            "body": (
                "Hi Avery, A provider delivery error caused my earlier note to reach you twice and I apologise for the inbox clutter. "
                "The relevant ask was: can you share one revenue operations area where a staffing constraint has become a bottleneck this quarter?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Acknowledge the duplicate send error, apologise once, and restate the single relevant ask.",
            "target_decision": "accept",
            "failure_rationale": "Ignoring or repeating after a duplicate send signals careless process management (P19) and erodes trust.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["revenue", "operations"],
            "forbidden_terms": ["ignore the previous", "disregard"],
            "banned_phrases": ["world-class", "quick chat", "sorry for any inconvenience"],
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
                "banned_condescension_absent",
                "expected_signal_term_present",
                "forbidden_terms_absent",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ],
            "judge_dimensions": ["next_step_quality", "style_guide_adherence", "output_validity"],
        },
        "metadata": {
            "probe_id": "P19",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out hard seed: duplicate-send reset; P19 multi-thread leakage failure mode.",
        },
    },
        # ── Original held_out specs below ─────────────────────────────────────────
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
                "Hi Priya, I do not want to imply frontend capacity we have not verified. The delivery scope I can support here is backend and data workflow work, so anything frontend-heavy should be routed to a human fit review first. "
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
    # ── Expansion held_out hard seeds (Wave 4) ───────────────────────────────
    {
        "partition": "held_out",
        "suffix": "gap-condescension-cto-skeptic",
        "difficulty": "hard",
        "failure_dimension": "gap_condescension",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Meridian Analytics",
                "contact_role": "CTO",
                "company_stage": "series_b",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "competitor_gap",
                        "evidence": "A recent engineering blog post by the CTO explicitly critiques AI vendor overselling and calls for proof-before-pitch evaluation standards.",
                        "confidence": "low",
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
            "prior_thread": {
                "contacted_before": False,
                "summary": "",
            },
        },
        "candidate_output": {
            "subject": "Re: evaluation-first approach",
            "body": (
                "Hi Maya, I read your post on proof-before-pitch evaluation standards and I want to be direct: "
                "I am not here to oversell a capability gap. "
                "Can you share one engineering area where an external staffing question has come up recently, "
                "so I can determine whether there is actually a relevant fit to evaluate?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Acknowledge the CTO's documented skepticism; make the pitch interrogative rather than assertive.",
            "target_decision": "accept",
            "failure_rationale": "Ignoring the CTO's published skepticism and framing a gap anyway is a gap-condescension failure.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["evaluation", "fit"],
            "forbidden_terms": ["falling behind", "competitors are ahead", "missing out"],
            "banned_phrases": ["world-class", "quick chat", "game-changing"],
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
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out: CTO's public skepticism of vendor overselling must redirect pitch to interrogative.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "ai-maturity-score-2-pilot",
        "difficulty": "hard",
        "failure_dimension": "ai_maturity_consistency",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Coral Health Systems",
                "contact_role": "VP Engineering",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_1_recently_funded",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "ai_maturity",
                        "evidence": "The engineering roadmap references a pilot ML pipeline for patient triage that is in active staging, not yet in production.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P24",
                    }
                ],
                "ai_maturity": {"score": 2, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "ml"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The VP Engineering confirmed the triage pipeline is in staging and asked about augmentation capacity.",
            },
        },
        "candidate_output": {
            "subject": "Re: staging-phase augmentation",
            "body": (
                "Hi Jordan, Given the triage pipeline is in active staging rather than fully productionised, "
                "the augmentation framing that makes most sense is capacity for staging workflow validation, not scale-out. "
                "Can you share what the current staging bottleneck looks like so I can assess the right support profile?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Stay at ai_maturity score 2 (pilot/staging); do not assume production-scale framing.",
            "target_decision": "accept",
            "failure_rationale": "Treating a staging pipeline as production-ready and framing scale-out capacity overshoots the declared maturity level.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["staging", "augmentation"],
            "forbidden_terms": ["fully deployed", "at scale", "production rollout"],
            "banned_phrases": ["world-class", "quick chat", "exciting opportunity"],
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
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out: staging pipeline must stay at score-2 language, not assume production capacity.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "ai-maturity-score-0-no-signal",
        "difficulty": "hard",
        "failure_dimension": "ai_maturity_consistency",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Granite Federal Solutions",
                "contact_role": "Chief of Staff",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_2_restructuring_cost",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "job_post_velocity",
                        "evidence": "No AI, automation, or workflow tooling signals are visible in public postings. All job posts reference manual contract review processes.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P24",
                    }
                ],
                "ai_maturity": {"score": 0, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": False,
                "summary": "",
            },
        },
        "candidate_output": {
            "subject": "Question on contract review load",
            "body": (
                "Hi Cassandra, Based on what I can see publicly, I have no signal about your current automation posture. "
                "Can you share whether contract review volume has created any resourcing pressure this quarter?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "With ai_maturity=0, abstain from all AI or automation capability claims; ground entirely in a resourcing question.",
            "target_decision": "accept",
            "failure_rationale": "Assuming AI interest when the score is 0 and no public signal exists is an ai_maturity_consistency failure.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["contract", "resourcing"],
            "forbidden_terms": ["automation interest", "AI adoption", "digital transformation"],
            "banned_phrases": ["world-class", "quick chat", "future-proof"],
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
            "judge_dimensions": ["ai_maturity_consistency", "signal_grounding"],
        },
        "metadata": {
            "probe_id": "P24",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out: zero-AI-signal prospect; no AI maturity claims allowed.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "gap-condescension-early-founder",
        "difficulty": "hard",
        "failure_dimension": "gap_condescension",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Ember Labs",
                "contact_role": "CEO",
                "company_stage": "seed",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "job_post_velocity",
                        "evidence": "A single data operations job post appeared three weeks ago at a seed-stage company; founder is a repeat operator with two prior successful exits.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P33",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": False,
                "summary": "",
            },
        },
        "candidate_output": {
            "subject": "Question on data operations",
            "body": (
                "Hi Priya, I noticed a data operations post and wanted to ask rather than assume: "
                "Can you share whether the ops capacity gap is something you are actively scoping, or is the timing still early?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Frame the gap as a research question, not an assumed deficiency; respect the founder's experience.",
            "target_decision": "accept",
            "failure_rationale": "Assuming the seed-stage founder has not yet addressed the gap is condescending toward an experienced repeat operator.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["data", "operations"],
            "forbidden_terms": ["you haven't addressed", "still struggling", "falling behind"],
            "banned_phrases": ["world-class", "quick chat", "early-stage struggles"],
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
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out: seed-stage repeat founder; gap must stay interrogative, not patronising.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "output-validity-email-channel-only",
        "difficulty": "medium",
        "failure_dimension": "output_validity",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Cascade Industries",
                "contact_role": "Director of Operations",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_2_restructuring_cost",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "prior_thread",
                        "evidence": "The prior note was sent via SMS without prior consent; the prospect responded asking to keep communication via email only.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P12",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "ops", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prospect explicitly requested email-only communication after receiving an unsolicited SMS.",
            },
        },
        "candidate_output": {
            "subject": "Re: communication preference noted",
            "body": (
                "Hi Theo, Noted on email-only going forward — the prior SMS was sent without confirming preference first and I will not repeat that. "
                "Can you share whether the operations restructuring question I raised is still worth a conversation?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Acknowledge the channel constraint explicitly; route all future contact to email as directed.",
            "target_decision": "accept",
            "failure_rationale": "Ignoring the prospect's explicit channel preference after an unsolicited SMS is an output_validity failure.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["email", "operations"],
            "forbidden_terms": ["SMS is fine", "any channel works"],
            "banned_phrases": ["world-class", "quick chat", "sorry for any inconvenience"],
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
                "banned_condescension_absent",
                "expected_signal_term_present",
                "forbidden_terms_absent",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ],
            "judge_dimensions": ["output_validity", "style_guide_adherence", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P12",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out: prospect requested email-only after unsolicited SMS; must acknowledge constraint.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "signal-grounding-linkedin-weak",
        "difficulty": "medium",
        "failure_dimension": "signal_grounding",
        "channel": "linkedin_dm",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Praxis Digital",
                "contact_role": "VP Sales Operations",
                "company_stage": "series_a",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_3_leadership_transition",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "job_post_velocity",
                        "evidence": "The only visible signal is that the VP liked two posts about revenue operations tooling on LinkedIn; no job posts, no press release, no public announcement.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P05",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "revops", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": False,
                "summary": "",
            },
        },
        "candidate_output": {
            "body": (
                "Hi Farid, I noticed some activity around RevOps tooling and wanted to ask rather than assume — "
                "Can you share whether the tooling question is actively on the roadmap, or more exploratory at this point?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Treat LinkedIn likes as weak signal; stay interrogative with explicit low-confidence framing.",
            "target_decision": "accept",
            "failure_rationale": "Asserting RevOps intent from two LinkedIn post likes is a signal_grounding failure.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["tooling", "roadmap"],
            "forbidden_terms": ["clearly interested", "you are actively looking", "obvious need"],
            "banned_phrases": ["world-class", "quick chat", "revolutionary"],
            "max_body_words": 120,
            "one_ask_required": True,
            "require_signal_reference": True,
            "confidence_aware_language": True,
            "forbid_bench_term": True,
            "allowed_channels": ["linkedin_dm"],
        },
        "scoring_config": {
            "deterministic_dimensions": [
                "output_nonempty",
                "max_body_words_respected",
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
            "probe_id": "P05",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out: LinkedIn post likes as signal — must stay interrogative, not assertive.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "style-guide-no-exclamation",
        "difficulty": "medium",
        "failure_dimension": "style_guide_adherence",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Solstice Capital",
                "contact_role": "Partner",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_1_recently_funded",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "funding_event",
                        "evidence": "Solstice closed a $40M Series C three months ago; headcount expansion posts suggest portfolio team growth.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P30",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "finance"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": False,
                "summary": "",
            },
        },
        "candidate_output": {
            "subject": "Question on portfolio team growth",
            "body": (
                "Hi Devon, The Series C close and the follow-on headcount activity suggest portfolio team capacity is on your mind. "
                "Can you share whether the growth is concentrated in one portfolio area or spread across the fund?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Draft must use level tone with no exclamation marks or enthusiasm markers; professional and grounded only.",
            "target_decision": "accept",
            "failure_rationale": "Exclamation marks and enthusiasm markers in outreach to a capital markets partner violate the Tenacious style guide.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["portfolio", "capacity"],
            "forbidden_terms": ["exciting", "thrilled", "amazing opportunity"],
            "banned_phrases": ["world-class", "quick chat", "love to connect"],
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
            "judge_dimensions": ["style_guide_adherence", "signal_grounding", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P30",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out: capital markets partner; enthusiasm markers and exclamation marks are prohibited.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "next-step-open-ended-rewrite",
        "difficulty": "medium",
        "failure_dimension": "next_step_quality",
        "channel": "email",
        "message_kind": "warm_reply",
        "input": {
            "prospect": {
                "company_name": "Quorum Technologies",
                "contact_role": "Head of Engineering",
                "company_stage": "series_b",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_3_leadership_transition",
                "signal_confidence": "medium",
                "signals": [
                    {
                        "signal_type": "leadership_change",
                        "evidence": "A new Head of Engineering joined six weeks ago following a reorg; the prior thread asked a broad question about current delivery priorities.",
                        "confidence": "medium",
                        "source_ref": "seed/probe_library.md#P34",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "medium"},
            },
            "bench_context": {
                "supported_stacks": ["python", "backend", "data"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": True,
                "summary": "The prior outreach used a vague CTA: 'let me know if you want to connect.' The new Head of Engineering did not reply.",
            },
        },
        "candidate_output": {
            "subject": "Re: delivery priorities after reorg",
            "body": (
                "Hi Sam, The reorg transition six weeks in often surfaces one delivery question that is harder to staff internally. "
                "Can you share the one backend or data area where you are most likely to need external capacity in the next quarter?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Replace the open-ended 'let me know' CTA with a specific, answerable question anchored in the leadership transition signal.",
            "target_decision": "accept",
            "failure_rationale": "An open-ended 'let me know if you want to connect' CTA is a next_step_quality failure — it creates no path for the buyer.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["delivery", "capacity"],
            "forbidden_terms": ["let me know", "whenever you are ready", "if interested"],
            "banned_phrases": ["world-class", "quick chat", "touch base"],
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
                "banned_condescension_absent",
                "expected_signal_term_present",
                "forbidden_terms_absent",
                "buyer_next_step_keyword_present",
                "single_ask_only",
            ],
            "judge_dimensions": ["next_step_quality", "signal_grounding", "style_guide_adherence"],
        },
        "metadata": {
            "probe_id": "P34",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out: open-ended CTA rewrite; must replace vague ask with specific answerable question.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "gap-condescension-incumbent-vendor",
        "difficulty": "hard",
        "failure_dimension": "gap_condescension",
        "channel": "linkedin_dm",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Nexus Pharma",
                "contact_role": "VP Technology",
                "company_stage": "mid_market",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_4_capability_gap",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "competitor_gap",
                        "evidence": "A public job post for a 'vendor evaluation lead' suggests an active assessment of their incumbent technology vendor, but the direction of the evaluation is unknown.",
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P33",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "data", "pharma"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": False,
                "summary": "",
            },
        },
        "candidate_output": {
            "body": (
                "Hi Lin, I noticed the vendor evaluation lead post and wanted to ask directly: "
                "is the evaluation focused on replacing capability, expanding it, or something else entirely? "
                "Can you share the direction of the evaluation so I do not assume the wrong fit?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Do not assume the incumbent vendor is failing; ask about the evaluation direction before positioning.",
            "target_decision": "accept",
            "failure_rationale": "Framing the gap as the incumbent's failure when the evaluation direction is unknown is a gap_condescension failure.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["evaluation", "vendor"],
            "forbidden_terms": ["your current vendor is failing", "falling behind on", "obviously need to switch"],
            "banned_phrases": ["world-class", "quick chat", "disruptive solution"],
            "max_body_words": 120,
            "one_ask_required": True,
            "require_signal_reference": True,
            "confidence_aware_language": True,
            "forbid_bench_term": True,
            "allowed_channels": ["linkedin_dm"],
        },
        "scoring_config": {
            "deterministic_dimensions": [
                "output_nonempty",
                "max_body_words_respected",
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
            "authoring_note": "Held-out: unknown vendor evaluation direction; must not assume incumbent is failing.",
        },
    },
    {
        "partition": "held_out",
        "suffix": "ai-maturity-conflicting-signals",
        "difficulty": "hard",
        "failure_dimension": "ai_maturity_consistency",
        "channel": "email",
        "message_kind": "cold_outreach",
        "input": {
            "prospect": {
                "company_name": "Tidal Operations",
                "contact_role": "VP Technology",
                "company_stage": "growth",
            },
            "hiring_signal_brief": {
                "primary_segment": "segment_3_leadership_transition",
                "signal_confidence": "low",
                "signals": [
                    {
                        "signal_type": "ai_maturity",
                        "evidence": (
                            "Two conflicting signals: a job post for 'ML platform engineer' suggests active AI adoption, "
                            "but a separate announcement describes 'reverting to manual approval workflows' for safety compliance."
                        ),
                        "confidence": "low",
                        "source_ref": "seed/probe_library.md#P24",
                    }
                ],
                "ai_maturity": {"score": 1, "confidence": "low"},
            },
            "bench_context": {
                "supported_stacks": ["python", "ml", "ops"],
                "capacity_commitment_allowed": False,
                "pricing_scope": "public_bands_only",
            },
            "prior_thread": {
                "contacted_before": False,
                "summary": "",
            },
        },
        "candidate_output": {
            "subject": "Question on ML and compliance posture",
            "body": (
                "Hi Natasha, I am seeing two signals that point in different directions: an ML platform hire and a shift toward manual approval workflow. "
                "Can you share which one reflects the current operational direction so I can understand whether a relevant fit exists?"
            ),
        },
        "ground_truth": {
            "expected_behavior": "Flag the contradictory signals explicitly; degrade ai_maturity to score 1 low-confidence; ask for clarification.",
            "target_decision": "accept",
            "failure_rationale": "Ignoring the conflicting signals and asserting an AI readiness level is an ai_maturity_consistency failure.",
        },
        "rubric": {
            "tone_markers": ["direct", "grounded", "honest", "professional"],
            "expected_terms": ["compliance", "workflow"],
            "forbidden_terms": ["clearly adopting AI", "obviously moving toward", "confirmed ML"],
            "banned_phrases": ["world-class", "quick chat", "cutting-edge AI"],
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
            "judge_dimensions": ["ai_maturity_consistency", "signal_grounding", "next_step_quality"],
        },
        "metadata": {
            "probe_id": "P24",
            "source_artifact": "seed/probe_library.md",
            "style_guide_version": "v2",
            "authoring_note": "Held-out: ML hire + manual-workflow revert; conflicting signals must degrade maturity score to 1 low-confidence.",
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
