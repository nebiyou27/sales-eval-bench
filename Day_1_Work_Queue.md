# Day 1 Work Queue

Date: 2026-04-28

Objective: complete Act I by turning Week 10 evidence into a concise audit memo and
locking the benchmark schema/evaluator path before Act II dataset construction.

## Ordered Queue

### 1. Finish `audit_memo.md`

Inputs:

- `seed/day1_seed_inventory.md`
- `seed/probe_library.md`
- `seed/failure_taxonomy.md`
- `methodology.md`

Acceptance criteria:

- Maximum 600 words.
- Cites at least eight probe IDs: P05, P24, P26, P27, P29, P30, P33, P35.
- Cites at least five trace examples from `seed/day1_seed_inventory.md`.
- Explains the exact Tenacious-specific benchmark gaps that generic public retail
  benchmarks miss.
- Ends with the Act I recommendation for Path B judge/critic work.

### 2. Tighten `schema.json`

Inputs:

- `schema.json`
- `tenacious_bench_v0.1/dev/dummy_tasks.jsonl`
- `synthesis_memos/synthetic_data_best_practices_v0.md`

Acceptance criteria:

- Three dummy tasks validate against the schema.
- Required metadata still covers partition, source mode, difficulty, failure dimension,
  source artifact, and probe ID.
- `retrieval_provenance` requirements are queued for any signal-grounded synthetic task.
- Schema dimensions remain aligned with `methodology.md`.

### 3. Verify `scoring/scoring_evaluator.py`

Inputs:

- `scoring/scoring_evaluator.py`
- `tenacious_bench_v0.1/dev/dummy_tasks.jsonl`

Acceptance criteria:

- `python scoring/scoring_evaluator.py` returns a passing smoke result.
- Each dummy task can produce a numeric deterministic score without human input.
- Any judge-backed fields remain optional hooks until Day 2 calibration.
- Failure cases remain visible rather than silently coerced into passes.

### 4. Lock Act I Evidence

Inputs:

- `seed/day1_seed_inventory.md`
- `seed/held_out_traces.jsonl`
- `seed/trace_log.jsonl`

Acceptance criteria:

- Audit memo references are traceable to files in `seed/`.
- Week 10 held-out trace IDs are used only as methodology evidence, not as training or dev
  preference examples.
- Candidate chosen/rejected examples remain flagged as provisional until manually inspected.

### 5. Prepare Act II Backlog

Inputs:

- `Day_Zero_Implementation_Plan.md`
- `synthesis_memos/synthetic_data_best_practices_v0.md`
- `cost_controls.md`

Acceptance criteria:

- Later-act tasks are separated from Day 1 work.
- Dataset generation starts from probe/trace templates, not open-ended bulk prompts.
- No eval-tier authoring or dedup is scheduled for Days 2-3.
- Contamination checking remains mandatory before held-out sealing.

## Public Benchmark Gaps To Name

- Generic retail benchmarks do not test Tenacious buyer-respect constraints for
  sophisticated AI buyers.
- They do not measure gap-condescension when public signals are weak or ambiguous.
- They do not require AI-maturity outputs to stay structured and usable.
- They do not test fixture/live-boundary failures from demo artifacts.
- They do not enforce account-level consistency across multi-thread prospect context.

## Day 1 Done Means

`audit_memo.md` is complete, `schema.json` and `scoring/scoring_evaluator.py` are verified on
dummy tasks, Act I evidence is traceable, and Act II starts with a controlled dataset-authoring
plan rather than a vague synthesis prompt.
