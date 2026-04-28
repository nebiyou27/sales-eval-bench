# Progress - Sales Eval Bench (TRP1 Week 11)

Decision log. Most recent entry first.

---

## 2026-04-28 - Repo layout refactor

**Completed:** Folder structure refactored before Day 1 work begins.

**Changes:**

- All project documentation moved into `docs/` (`PRD.md`, `methodology.md`, `progress.md`,
  `audit_memo.md`, `cost_controls.md`).
- `seed/day1_seed_inventory.md` moved to `docs/inventories/` so `seed/` stays read-only Week 10
  inputs.
- Synthesis memos consolidated under `docs/memos/`. Plans (`Day_Zero_Implementation_Plan.md`,
  `Day_1_Work_Queue.md`) consolidated under `docs/plans/`. Training plan moved to
  `docs/training/unsloth_smoke_test_plan.md`.
- Code reorganized under `src/` with `generation/`, `scoring/`, `training/`, `ablations/`
  subfolders. `scoring/scoring_evaluator.py` is now `src/scoring/scoring_evaluator.py`.
- `tenacious_bench_v0.1/smoke/` added; `dummy_orpo_preferences.jsonl` moved there so
  `tenacious_bench_v0.1/` is data-only and `src/training/` reserved for code.
- `cost/log.csv` replaces root-level `cost_log.csv`; gitignore updated accordingly.
- `tests/` directory created for upcoming unit tests.
- Stale `.gitkeep` files removed from folders that already contain real files.

**Verification:** `python src/scoring/scoring_evaluator.py` passes positive and negative cases.
`README.md` and `CLAUDE.md` directory indexes updated. All inter-doc references repointed.

**Why now:** Day 2-3 will land generation scripts and Day 5 will land training scripts. Once
those exist, refactoring the layout becomes expensive and risks broken imports. Doing it on
Day Zero is cheap.

**Next:** Begin Day 1 Act I against the new layout.

---

## 2026-04-28 - Day Zero Step 10 Day 1 queue

**Completed:** Day 1 work queue prepared and Day Zero readiness review closed.

**Artifacts:** `Day_1_Work_Queue.md` defines the ordered Act I execution queue and acceptance
criteria. `audit_memo.md` now exists as a Day 1 starter with the required probe and trace evidence.

**Confirmed Day 1 work surface:** `schema.json`, `scoring/scoring_evaluator.py`, and
`tenacious_bench_v0.1/dev/dummy_tasks.jsonl` are the schema/evaluator verification targets.

**Verification:** `python scoring/scoring_evaluator.py` passes. All three dummy tasks validate
against `schema.json` and receive passing numeric deterministic scores.

**Next:** Begin Day 1 Act I by writing the 600-word audit memo, then tighten schema/evaluator
checks against the three dummy tasks.

---

## 2026-04-28 - Day Zero Step 9 common-reading memo

**Completed:** First synthesis memo drafted from Liu et al., "Best Practices and Lessons
Learned on Synthetic Data" (`arXiv:2404.07503v2`).

**Artifact:** `synthesis_memos/synthetic_data_best_practices_v0.md`.

**Repo decision:** Days 2-3 synthesis should be controlled and metadata-rich: generate from
probe/trace templates, preserve source and failure-dimension metadata, filter before partition
assignment, and run contamination checks before held-out sealing. Generic high-quality synthetic
sales examples are not sufficient for Tenacious-Bench because a response can be factually
grounded but still fail buyer-respect or signal-entitlement constraints.

**Next:** Step 10 - prepare the Day 1 work queue.

---

## 2026-04-28 - Day Zero readiness through Step 8

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
preference examples. `training/unsloth_smoke_test_plan.md` schedules a Colab T4 Qwen3-0.6B Unsloth
smoke run with fp16, Qwen3-1.7B as fallback only after a stable T4 run, and optional HuggingFace adapter push.

**Cost tracking:** `cost_log.csv` and `cost_controls.md` are live. The Week 11 cap is USD 10:
USD 3-5 for dataset authoring, USD 0-5 for training, USD 2-3 for held-out evaluation, and
USD 1-2 reserve. No tau2-Bench retail reruns and no eval-tier authoring or dedup on Days 2-3.

**Next:** Step 9 - draft or queue the first common-reading memo.

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
