"""Committed synthesis prompts and model-rotation policy for Tenacious-Bench."""

from __future__ import annotations

import json
from typing import Any


PROMPT_VERSION = "v1"

DEFAULT_GENERATION_MODEL = "qwen/qwen3-next-80b-a3b-instruct"
DEFAULT_JUDGE_MODEL = "deepseek/deepseek-chat"

SYSTEM_PROMPT = """You are authoring Tenacious-Bench v0.1 benchmark tasks.
Return exactly one JSON object matching the local schema for each request.
The task must:
- be Tenacious-specific B2B sales work, not generic retail
- use channel=email
- use subject/body output format
- keep one ask only
- preserve Tenacious style markers: direct, grounded, honest, professional, non-condescending where relevant
- include metadata.style_guide_version="v2"
- include metadata.retrieval_provenance when source_mode=synthetic and failure_dimension=signal_grounding
- set ground_truth.target_decision to accept, revise, or block
- use source_mode=synthetic
Do not wrap the JSON in markdown fences."""

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
    return f"""Create one schema-valid Tenacious-Bench task.
Task id stem: {partition}-synthetic-{index:03d}-{spec['task_id_stub']}
Focus: {spec['focus']}
Probe ID: {spec['probe_id']}
Failure dimension: {spec['failure_dimension']}
Message kind: {spec['message_kind']}
Partition: {partition}
Use the current schema fields and include explicit signal evidence, bench context, prior thread context, and a strict rubric.
The candidate output should be realistic outreach, not a placeholder."""


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
