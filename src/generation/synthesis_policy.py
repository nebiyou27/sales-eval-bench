"""Committed synthesis prompts and model-rotation policy for Tenacious-Bench."""

from __future__ import annotations

import json
from typing import Any


PROMPT_VERSION = "v1"

DEFAULT_GENERATION_MODEL = "qwen/qwen3-next-80b-a3b-instruct"
DEFAULT_JUDGE_MODEL = "deepseek/deepseek-chat"

SYSTEM_PROMPT = """\
You are authoring Tenacious-Bench v0.1 benchmark tasks.
Return exactly one valid JSON object for each request. No markdown fences. No extra keys.

REQUIRED TOP-LEVEL STRUCTURE (additionalProperties=false — use only these keys):
{
  "task_id": "<string>",
  "partition": "<train|dev|held_out>",
  "source_mode": "synthetic",
  "difficulty": "<easy|medium|hard>",
  "failure_dimension": "<output_validity|ai_maturity_consistency|gap_condescension|signal_grounding|style_guide_adherence|next_step_quality>",
  "channel": "<email|linkedin_dm|sms>",
  "message_kind": "<cold_outreach|warm_reply|reengagement>",
  "input": {
    "prospect": {"company_name": "<str>", "contact_role": "<str>", "company_stage": "<str>"},
    "hiring_signal_brief": {
      "primary_segment": "<segment_1_recently_funded|segment_2_restructuring_cost|segment_3_leadership_transition|segment_4_capability_gap>",
      "signal_confidence": "<low|medium|high>",
      "signals": [{"signal_type": "<funding_event|job_post_velocity|layoff_event|leadership_change|competitor_gap|ai_maturity|bench_match|pricing_scope|prior_thread>", "evidence": "<str>", "confidence": "<low|medium|high>", "source_ref": "<str>"}],
      "ai_maturity": {"score": 0, "confidence": "<low|medium|high>"}
    },
    "bench_context": {"supported_stacks": ["<str>"], "capacity_commitment_allowed": false, "pricing_scope": "<public_bands_only|route_specific_quote_to_human>"},
    "prior_thread": {"contacted_before": false, "summary": "<str or empty string>"}
  },
  "candidate_output": {"subject": "<str, required for email>", "body": "<str>"},
  "ground_truth": {"expected_behavior": "<str>", "target_decision": "accept", "failure_rationale": "<str>"},
  "rubric": {
    "tone_markers": ["direct", "grounded", "honest", "professional"],
    "expected_terms": ["<term1>", "<term2>"],
    "forbidden_terms": ["<term>"],
    "banned_phrases": ["world-class", "quick chat"],
    "max_body_words": 120,
    "max_subject_chars": 60,
    "one_ask_required": true,
    "require_signal_reference": true,
    "confidence_aware_language": true,
    "forbid_bench_term": true,
    "allowed_channels": ["email"]
  },
  "scoring_config": {
    "deterministic_dimensions": ["output_nonempty", "subject_present_for_email", "max_body_words_respected", "max_subject_chars_respected", "banned_phrase_absent", "bench_term_absent", "banned_condescension_absent", "expected_signal_term_present", "forbidden_terms_absent", "buyer_next_step_keyword_present", "single_ask_only"],
    "judge_dimensions": ["<failure_dimension>"]
  },
  "metadata": {
    "probe_id": "P##",
    "source_artifact": "seed/probe_library.md",
    "style_guide_version": "v2",
    "retrieval_provenance": {"url": "<URI>", "retrieved_at": "2024-01-01T00:00:00Z", "source_type": "<str>"}
  }
}

RULES:
- source_mode must always be "synthetic".
- Do NOT add any top-level key not in the structure above.
- For email channel: candidate_output must have both "subject" and "body"; rubric must have "max_subject_chars".
- For non-email channel: omit "subject" from candidate_output; omit "max_subject_chars" and "subject_present_for_email"/"max_subject_chars_respected" from scoring_config.
- For failure_dimension=signal_grounding: metadata.retrieval_provenance is required (object, not a string).
- max_body_words: cold_outreach ≤ 120, warm_reply ≤ 200, reengagement ≤ 100.
- candidate_output.body must contain exactly one sentence with a CTA keyword (schedule/book/call/demo/meet/reply/send/share/next step/talk).
- expected_terms must both appear in candidate_output.body.
- forbidden_terms must NOT appear in candidate_output.body.
- banned_phrases must NOT appear in candidate_output.body.
- Do NOT use the word "bench" or "Tenacious" in candidate_output.body (forbidden by bench_term_absent check).
- Do NOT use words: obviously, simply, just need to, you don't understand, basic, easy (condescension check).
- metadata.probe_id must match the pattern P[0-9]{2} exactly (e.g. "P05", "P33").

EXAMPLE (copy the structure exactly, not the content):
{"task_id":"train-programmatic-007-thin-signal-restraint","partition":"train","source_mode":"programmatic","difficulty":"easy","failure_dimension":"signal_grounding","channel":"email","message_kind":"cold_outreach","input":{"prospect":{"company_name":"QuarryOS","contact_role":"COO","company_stage":"mid_market"},"hiring_signal_brief":{"primary_segment":"segment_2_restructuring_cost","signal_confidence":"low","signals":[{"signal_type":"job_post_velocity","evidence":"A few public hiring signals are visible, but they are still too thin to claim a real workflow queue issue.","confidence":"low","source_ref":"seed/probe_library.md#P29"}],"ai_maturity":{"score":1,"confidence":"medium"}},"bench_context":{"supported_stacks":["python","data"],"capacity_commitment_allowed":false,"pricing_scope":"public_bands_only"},"prior_thread":{"contacted_before":false,"summary":""}},"candidate_output":{"subject":"Question on workflow load","body":"Hi Rafael, A few public hiring signals are visible, but they are still too thin to claim a real workflow queue issue. Can you share one place where the workflow queue actually slows down if the outside signal is missing something?"},"ground_truth":{"expected_behavior":"Use interrogative, low-confidence language when the visible signal is thin.","target_decision":"accept","failure_rationale":"Weak public evidence should not become a confident prospect narrative."},"rubric":{"tone_markers":["direct","grounded","honest","professional"],"expected_terms":["workflow","queue"],"forbidden_terms":["obviously"],"banned_phrases":["quick question","world-class","synergize"],"max_body_words":120,"one_ask_required":true,"require_signal_reference":true,"confidence_aware_language":true,"forbid_bench_term":true,"allowed_channels":["email"],"max_subject_chars":60},"scoring_config":{"deterministic_dimensions":["output_nonempty","subject_present_for_email","max_body_words_respected","max_subject_chars_respected","banned_phrase_absent","bench_term_absent","banned_condescension_absent","expected_signal_term_present","forbidden_terms_absent","buyer_next_step_keyword_present","single_ask_only"],"judge_dimensions":["signal_grounding","style_guide_adherence","next_step_quality"]},"metadata":{"probe_id":"P29","source_artifact":"seed/probe_library.md","style_guide_version":"v2"}}
"""

JUDGE_SYSTEM_PROMPT = """You are the synthesis gate for Tenacious-Bench v0.1.
You must judge whether a candidate synthetic task is safe to keep for benchmark construction.
Reject generic sales tasks, tasks that weaken Tenacious-specific buyer-respect constraints, and tasks
that appear too close to other benchmark items or their own candidate output.
Return exactly one JSON object with:
- decision: accept, revise, or block
- confidence: low, medium, or high
- reasons: array of short strings
- required_fixes: array of short strings
Use decision=accept only if the task is Tenacious-specific, schema-shaped, non-generic, and suitable
for downstream benchmark use. Do not return markdown fences."""


def build_generation_prompt(spec: dict[str, Any], index: int, partition: str) -> str:
    channel = spec.get("channel", "email")
    return f"""Create one schema-valid Tenacious-Bench task following the EXACT structure in the system prompt.
Set task_id to: {partition}-synthetic-{index:03d}-{spec['task_id_stub']}
Set partition to: {partition}
Set source_mode to: synthetic
Set channel to: {channel}
Set message_kind to: {spec['message_kind']}
Set failure_dimension to: {spec['failure_dimension']}
Set metadata.probe_id to: {spec['probe_id']}
Focus: {spec['focus']}
Produce realistic B2B Tenacious outreach. The candidate_output.body must satisfy all rubric checks (expected_terms present, forbidden_terms absent, banned_phrases absent, single CTA, no condescension words, no bench/Tenacious in body).
Return only the JSON object, no markdown."""


def build_judge_prompt(task: dict[str, Any]) -> str:
    return (
        "Review this synthetic Tenacious-Bench task candidate for benchmark admission.\n"
        "Check that it is Tenacious-specific, non-generic, respectful to sophisticated buyers, and worth keeping.\n"
        "Candidate task JSON:\n"
        f"{json.dumps(task, ensure_ascii=True, sort_keys=True)}"
    )


def model_family(model_name: str) -> str:
    normalized = model_name.strip().lower()
    if "qwen" in normalized:
        return "qwen"
    if "deepseek" in normalized:
        return "deepseek"
    if "claude" in normalized:
        return "claude"
    if normalized.startswith("gpt") or "openai" in normalized:
        return "gpt"
    if "/" in normalized:
        return normalized.split("/", 1)[0]
    return normalized.split("-", 1)[0]


def enforce_rotation(generate_model: str, judge_model: str) -> None:
    generation_family = model_family(generate_model)
    judge_family = model_family(judge_model)
    if generation_family == judge_family:
        raise ValueError(
            "R2 rotation policy violation: the same model family cannot both generate and judge a task "
            f"({generation_family})."
        )
