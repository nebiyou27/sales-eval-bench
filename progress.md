# Progress - Sales Eval Bench (TRP1 Week 11)

Decision log. Most recent entry first.

---

## 2026-04-28 - Day Zero readiness through Step 7

**Completed:** Accounts, local environment, seed inventory, schema starter, evaluator smoke path,
and scheduled Unsloth training smoke test.

**Access and secrets:** HuggingFace, OpenRouter, and Colab T4 access are ready. `.env` remains
ignored; `.env.example` contains only empty placeholders.

**Local environment:** Python 3.11+ `.venv` is active, dependencies install from
`requirements.txt`, and `transformers`, `peft`, `trl`, `datasets`, `accelerate`, and
`bitsandbytes` import successfully.

**Evaluator/schema:** `schema.json` exists, `scoring/scoring_evaluator.py` returns numeric scores,
and `tenacious_bench_v0.1/dev/dummy_tasks.jsonl` validates with three passing dummy tasks.

**Seed inventory:** `seed/day1_seed_inventory.md` maps Week 10 probes and traces to Day 1 audit
work, including candidate chosen/rejected examples for Path B preference data.

**Training smoke test:** `training/dummy_orpo_preferences.jsonl` contains five valid ORPO
preference examples. `training/unsloth_smoke_test_plan.md` schedules a Colab T4 Qwen3.5 Unsloth
smoke run with fp16, no QLoRA 4-bit, and optional HuggingFace adapter push.

**Next:** Step 8 - create `cost_log.csv` and lock the USD 10 budget buckets.

---

## 2026-04-27 - Project scaffolded

**Decision:** Path B (ORPO preference-tuned judge/critic).

**Why:** Week 10 produced two measured failure modes: P33 gap-condescension (15.6% A/B) and
P24 AI-maturity empty JSON (43.3% tau2). Both are inconsistency failures: the agent is
sometimes right but cannot detect when it is wrong. A trained judge/critic directly addresses
self-detection. Path A (SFT) would improve average output quality but not catch bad outputs.
Path C (PRM) requires multi-turn trajectory data not available at scale.

**Algorithm:** ORPO over DPO or SimPO. Rationale: reference-free, single-stage, fits T4 16 GB
VRAM, no length-normalization tuning needed for short sales-outreach outputs.

**Seed artifacts copied from Week 10:**

- `seed/trace_log.jsonl` (31 KB) - real agent outputs
- `seed/probe_library.md` - 35 probes across 11 failure categories
- `seed/failure_taxonomy.md` - measured trigger rates
- `seed/held_out_traces.jsonl` - 17 tau2 evaluatable traces

**Next:** Act I - `audit_memo.md`, `schema.json`, `scoring_evaluator.py`.
