"""Generate Week 10 Conversion Engine baseline predictions for held-out tasks.

Calls build_commitment_email() from the Week 10 engine directly, bypassing the
full evidence/claims/judgment pipeline (which needs live fixtures and API calls).
Maps each held-out task's structured input to a minimal claim set, then runs the
Week 10 email draft function to produce {subject, body} output.

The resulting JSONL is the --baseline-predictions file for run_ablation.py.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

WEEK10_ENGINE_ROOT = Path("D:/TRP-1/week-10/Conversion Engine")
REPO_ROOT = Path(__file__).resolve().parents[2]
HELD_OUT_DIR = REPO_ROOT / "tenacious_bench_v0.1" / "held_out"
OUTPUT_PATH = REPO_ROOT / "reports" / "baseline_predictions.jsonl"

# Add Week 10 engine to path so we can import its modules.
sys.path.insert(0, str(WEEK10_ENGINE_ROOT))


CONFIDENCE_TO_TIER: dict[str, str] = {
    "high": "corroborated",
    "medium": "corroborated",
    "low": "inferred",
    "very_low": "inferred",
}

# Normalise short segment labels that may appear in task inputs.
SEGMENT_ALIASES: dict[str, str] = {
    "s4": "segment_4_specialized_capability",
    "s3": "segment_3_leadership_transition",
    "s2": "segment_2",
    "s1": "segment_1",
    "segment_4": "segment_4_specialized_capability",
    "segment_3": "segment_3_leadership_transition",
}


def build_claims(task: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert a held-out task's input signals into Week 10 claim rows."""
    inp = task.get("input", {})
    brief = inp.get("hiring_signal_brief", {})
    prospect = inp.get("prospect", {})
    signals: list[str] = brief.get("signals", [])
    confidence = brief.get("signal_confidence", "medium")
    tier = CONFIDENCE_TO_TIER.get(str(confidence).lower(), "inferred")

    claims: list[dict[str, Any]] = []
    for i, sig in enumerate(signals, 1):
        # Signals may be dicts {signal_type, evidence, confidence, source_ref} or plain strings.
        if isinstance(sig, dict):
            assertion = sig.get("evidence") or sig.get("signal_type") or str(sig)
        else:
            assertion = str(sig)
        claims.append({
            "kind": "hiring_surge",
            "claim_id": f"c{i:03d}",
            "assertion": assertion,
            "tier": tier,
        })

    stage = prospect.get("company_stage", "")
    if stage:
        claims.append({
            "kind": "funding_round",
            "claim_id": "c_stage",
            "assertion": f"Company at {stage} stage",
            "tier": "corroborated",
        })

    if not claims:
        claims.append({
            "kind": "company_metadata",
            "claim_id": "c000",
            "assertion": "Active hiring observed",
            "tier": "inferred",
        })
    return claims


def map_segment(task: dict[str, Any]) -> str:
    raw = str(task.get("input", {}).get("hiring_signal_brief", {}).get("primary_segment", "")).lower()
    return SEGMENT_ALIASES.get(raw, raw) or "segment_unknown"


def generate_one(
    task: dict[str, Any],
    build_fn: Any,
    bench_error_cls: type[Exception],
) -> dict[str, Any] | None:
    company_name = task.get("input", {}).get("prospect", {}).get("company_name", "Unknown")
    segment = map_segment(task)
    claims = build_claims(task)

    bench_ctx = task.get("input", {}).get("bench_context", {})
    bench_summary_id: str | None = (
        "bench_summary_placeholder" if bench_ctx.get("capacity_commitment_allowed") else None
    )

    t0 = time.monotonic()
    for attempt_bench_id in (bench_summary_id, "bench_summary_placeholder", None):
        try:
            result = build_fn(
                company_name=company_name,
                prospect_name=None,
                claim_rows=claims,
                segment_match=segment,
                bench_summary_id=attempt_bench_id,
            )
            break
        except bench_error_cls:
            continue
        except Exception as exc:
            print(f"  SKIP {task.get('task_id')}: {type(exc).__name__}: {exc}", file=sys.stderr)
            return None
    else:
        print(f"  SKIP {task.get('task_id')}: exhausted bench_summary_id attempts", file=sys.stderr)
        return None

    latency_ms = (time.monotonic() - t0) * 1000
    return {
        "task_id": task["task_id"],
        "candidate_output": {
            "subject": result.get("subject", ""),
            "body": result.get("body", ""),
        },
        "latency_ms": round(latency_ms, 1),
        "input_tokens": 0,
        "output_tokens": 0,
        "usd_cost": 0.0,
    }


def load_tasks() -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for path in sorted(HELD_OUT_DIR.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    return tasks


def main() -> int:
    try:
        from agent.actions.email_draft import build_commitment_email  # type: ignore
        # Discover the BenchCommitmentError class; fall back to a base exception if absent.
        try:
            from agent.actions.email_draft import BenchCommitmentError  # type: ignore
        except ImportError:
            BenchCommitmentError = ValueError  # type: ignore[assignment,misc]
    except ImportError as exc:
        print(
            f"Cannot import Week 10 engine from {WEEK10_ENGINE_ROOT}.\n"
            f"Check the path and that the venv has the Week 10 dependencies installed.\n"
            f"Error: {exc}",
            file=sys.stderr,
        )
        return 1

    tasks = load_tasks()
    print(f"Loaded {len(tasks)} held-out tasks from {HELD_OUT_DIR}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    skipped = 0
    with OUTPUT_PATH.open("w", encoding="utf-8") as fh:
        for task in tasks:
            row = generate_one(task, build_commitment_email, BenchCommitmentError)
            if row:
                fh.write(json.dumps(row) + "\n")
                written += 1
            else:
                skipped += 1

    print(f"Done - wrote {written} predictions, skipped {skipped} -> {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
