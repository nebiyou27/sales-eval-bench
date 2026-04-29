# Progress - Sales Eval Bench (TRP1 Week 11)

Decision log. Most recent entry first.

---

## 2026-04-29 - Contamination check upgraded to real embeddings with honest fallback

**Completed:** The contamination checker now attempts a real local embedding pass instead of
claiming only a proxy path.

**Changes:**

- Upgraded `src/generation/contamination_check.py` to try
  `sentence-transformers/all-MiniLM-L6-v2` through the local `transformers` stack.
- Added cosine-similarity scoring over sentence embeddings while keeping 8-gram overlap and
  lexical cosine as supporting signals.
- Added explicit report fields for `embedding_model`, `embedding_cosine_threshold`, and
  `embedding_check_status` so the output states whether embeddings truly ran.
- Added unit tests for both the completed-embedding path and the unavailable-model fallback path.

**Verification:** `& .\.venv\Scripts\python.exe -m unittest tests.test_contamination_check` passes.
`& .\.venv\Scripts\python.exe src/generation/contamination_check.py` now reports
`train=2`, `dev=8`, `held_out=2`, and `pass=true`.

**Scope note:** The code path is now real, but this machine does not yet have the MiniLM weights
cached locally, so the current report honestly shows `embedding_check_unavailable:OSError`
instead of pretending the embedding pass succeeded.

**Next:** Update repo-facing docs to match the implemented authoring, rotation, and contamination
state.

---

## 2026-04-29 - Hand-authored generator and partition seeds added

**Completed:** The fourth Week 11 authoring mode is now runnable, and `train/` is no longer an
empty placeholder.

**Changes:**

- Added `generate_hand_authored.py` with explicit hand-authored tasks grounded in Week 10 probe
  definitions.
- Added two `train` tasks covering P26 fabricated-source risk and P27 peer-gap abstention.
- Added two local `held_out` tasks covering P32 bench-capacity over-commitment and P35
  multi-contact account framing consistency.
- Added generator tests and removed the stale `train/.gitkeep` placeholder.

**Verification:** `& .\.venv\Scripts\python.exe src/generation/generate_hand_authored.py --partition train`
writes `tenacious_bench_v0.1/train/hand_authored_tasks.jsonl`. The corresponding unit test passes.

**Scope note:** `tenacious_bench_v0.1/held_out/` remains gitignored by repo policy, so the local
held-out seeds exist for contamination and eval scaffolding but are not pushed to the remote.

**Next:** Replace the contamination lexical proxy with a real local embedding path while keeping an
honest fallback state.

---

## 2026-04-29 - Synthesis judge policy and R2 rotation enforcement added

**Completed:** The synthesis pipeline now has committed prompts, code-enforced generate/judge
family separation, and a live judge-filter path.

**Changes:**

- Added `synthesis_policy.py` with committed generation and judge prompts, prompt versioning, model
  family detection, and `enforce_rotation(...)`.
- Updated `generate_synthesis.py` to stamp prompt/model metadata, require a distinct judge model in
  live mode, log live synthesis calls, and persist judge rejections separately.
- Added unit tests for model-family normalization and rotation-policy enforcement.

**Verification:** `py_compile` passes for the synthesis modules, the synthesis-policy unit tests
pass, and `& .\.venv\Scripts\python.exe src/generation/generate_synthesis.py` regenerates the
offline prompt manifest with the committed prompt version and judge-model metadata.

**Scope note:** The live synthesis path is implemented, but no OpenRouter budget has been spent in
this repo pass; the default verification remains offline prompt-manifest generation.

**Next:** Add the missing hand-authored authoring mode and start filling `train/`.

---

## 2026-04-29 - Trace-derived task generation added

**Completed:** The third Week 11 authoring mode is now runnable under `src/generation/`.

**Changes:**

- Added `generate_trace_derived.py` with an explicit audited mapping from Week 10 failed trace IDs
  to schema-valid Tenacious-Bench tasks.
- Enforced held-out protection in code by blocking any trace ID found in `seed/held_out_traces.jsonl`
  from entering `train` or `dev`.
- Preserved provenance metadata including `source_trace_ids`, original task IDs, trace reward, and
  a derivation note that makes the reconstruction boundary explicit.
- Updated `README.md` run order to include the new trace-derived generation path.

**Verification:** `python src/generation/generate_trace_derived.py` writes
`tenacious_bench_v0.1/dev/trace_derived_tasks.jsonl` with schema-valid tasks and audited source
trace IDs from `seed/trace_log.jsonl`.

**Scope note:** At the time of this entry, the runnable authoring modes covered 3 of the 4 Week 11
paths: trace-derived, programmatic, and synthesis scaffold. Hand-authored adversarial tasks and
live judge-filtering were still pending.

**Next:** Add judge-filter logic and committed prompts for synthesis, then start filling
`train/` and `held_out/` with partition-safe tasks.

---

## 2026-04-29 - Dataset authoring scaffolds added

**Completed:** First-pass generation scaffolds now exist under `src/generation/`.

**Changes:**

- Added `generate_programmatic.py` with schema-validated Tenacious task templates.
- Added `generate_synthesis.py` in offline prompt-manifest mode by default, with optional live
  OpenRouter generation later.
- Added `contamination_check.py` with honest scaffold status and machine-readable report output.
- Added shared JSONL/schema helpers in `common.py`.
- Expanded programmatic coverage to include P24, P29, P30, and P33, each with source trace IDs.

**Verification:** `python src/generation/generate_programmatic.py` emits schema-valid tasks.
`python src/generation/generate_synthesis.py` emits a prompt manifest without spending API budget.
`python src/generation/contamination_check.py` writes a report and now distinguishes
`pending_no_held_out_data` from a clean checked held-out partition.

**Scope note:** At the time of this entry, this scaffold covered 2 of the 4 Week 11 authoring
modes in runnable code: programmatic and synthesis. Trace-derived and hand-authored authoring were
still pending.

**Next:** Expand the task batch, add trace-derived task generation, and wire the live synthesis
path to judge-filtering and cost logging.

---

## 2026-04-29 - Python 3.11 environment repaired

**Completed:** The Day Zero local-environment blocker is now closed with a fresh Python 3.11
virtual environment.

**Changes:**

- Installed Python 3.11.9 locally and rebuilt `.venv` against `py -3.11`.
- Reinstalled the pinned dependencies from `requirements.txt`.
- Re-ran the import proof for `transformers`, `peft`, `trl`, `datasets`, `accelerate`, and
  `bitsandbytes`.
- Re-ran the local evaluator smoke command on the rebuilt environment.

**Verification:** `& .\.venv\Scripts\python.exe --version` returns `Python 3.11.9`.
`python -c "import transformers, peft, trl, datasets, accelerate, bitsandbytes; print(transformers.__version__, peft.__version__, trl.__version__, datasets.__version__, accelerate.__version__, bitsandbytes.__version__)"` prints `5.6.2 0.19.1 1.3.0 4.8.5 1.13.0 0.49.2`.
`python src/scoring/scoring_evaluator.py` returns `"smoke_passed": true`.

**Why now:** The earlier Day Zero record incorrectly assumed Python 3.11+ was already active.
Closing that gap before more dependency or dataset-authoring work keeps the environment proof honest.

**Next:** Continue Day 1 Act I with `docs/audit_memo.md`, schema tightening, and dataset-authoring script scaffolding.

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
`tenacious_bench_v0.1/smoke/dummy_tasks.jsonl` are the schema/evaluator verification targets.

**Verification:** `python scoring/scoring_evaluator.py` passes. All three dummy tasks in
`tenacious_bench_v0.1/smoke/dummy_tasks.jsonl` validate against `schema.json` and receive passing
numeric deterministic scores.

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
and `tenacious_bench_v0.1/smoke/dummy_tasks.jsonl` validates with three passing dummy tasks.

**Seed inventory:** `seed/day1_seed_inventory.md` maps Week 10 probes and traces to Day 1 audit
work, including candidate chosen/rejected examples for Path B preference data.

**Training smoke test:** `training/dummy_orpo_preferences.jsonl` contains five valid ORPO
preference examples. `training/unsloth_smoke_test_plan.md` schedules a Colab T4 Qwen3-0.6B Unsloth
smoke run with fp16, Qwen3-1.7B as fallback only after a stable T4 run, and optional HuggingFace adapter push.

**Cost tracking:** `cost/log.csv` and `cost_controls.md` are live. The Week 11 cap is USD 10:
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
