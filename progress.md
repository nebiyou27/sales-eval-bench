# Progress — Sales Eval Bench (TRP1 Week 11)

Decision log. Most recent entry first.

---

## 2026-04-27 — Project scaffolded

**Decision:** Path B (ORPO preference-tuned judge/critic).

**Why:** Week 10 produced two measured failure modes — P33 gap-condescension (15.6% A/B) and
P24 AI-maturity empty JSON (43.3% tau2). Both are inconsistency failures: the agent is
sometimes right but cannot detect when it is wrong. A trained judge/critic directly addresses
self-detection. Path A (SFT) would improve average output quality but not catch bad outputs.
Path C (PRM) requires multi-turn trajectory data not available at scale.

**Algorithm:** ORPO over DPO or SimPO. Rationale: reference-free, single-stage, fits T4 16 GB
VRAM, no length-normalization tuning needed for short sales-outreach outputs.

**Seed artifacts copied from Week 10:**
- `seed/trace_log.jsonl` (31 KB) — real agent outputs
- `seed/probe_library.md` — 35 probes across 11 failure categories
- `seed/failure_taxonomy.md` — measured trigger rates
- `seed/held_out_traces.jsonl` — 17 tau2 evaluatable traces

**Next:** Act I — audit_memo.md, schema.json, scoring_evaluator.py
