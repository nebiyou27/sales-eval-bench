# Day Zero Implementation Plan

Project: Tenacious-Bench Sales Agent Evaluation Bench  
Date: 2026-04-27  
Source brief: `Challenge_Documents/TRP1 Challenge Week 11_  Sales Agent Evaluation Bench.docx`  
Current path decision: Path B, ORPO preference-tuned judge / critic

## Day Zero Objective

Finish the pre-flight work required to start Act I cleanly: accounts and keys are ready, the local environment can run the benchmark tooling, Week 10 seed artifacts are inventoried, the evaluation path is declared, cost tracking exists, and the first reading memo is drafted.

Day Zero is successful when the Day 1 readiness review can answer yes to this question:

```text
Can Acts I-II begin without access, environment, scope, or path-selection blockers?
```

## Four-Hour Execution Schedule

| Timebox | Focus | Output |
|---|---|---|
| 0:00-0:20 | Repo and brief orientation | Confirm challenge requirements, current path, and existing files |
| 0:20-0:55 | Accounts and credentials | HuggingFace, OpenRouter, Colab, optional RunPod readiness |
| 0:55-1:35 | Local environment | Python 3.11+, packages, schema validation stub, evaluator command path |
| 1:35-2:10 | Week 10 artifact inventory | Parseable seed files and trace/probe coverage notes |
| 2:10-2:45 | Training compute smoke test | Unsloth dummy LoRA run plan and HuggingFace push check |
| 2:45-3:15 | Cost tracking and budget controls | Cost log with buckets and hard caps |
| 3:15-3:45 | First reading memo | Draft v0 synthesis memo for one common reading |
| 3:45-4:00 | Readiness review | Blocker list, Day 1 task queue, owner decisions |

## Checklist

### 1. Confirm The Week 11 Mission

- [x] Re-read the challenge brief and capture the required final outcome.
- [x] Confirm the project is not a generic sales benchmark; it is Tenacious-specific.
- [x] Confirm no new tau2-Bench retail validation run will be performed this week.
- [x] Confirm the new Tenacious-Bench score is the primary baseline if Week 10 tau2 score is unavailable.
- [x] Confirm the hardest work is dataset construction, not the training run.
- [x] Confirm public artifacts are required: HuggingFace dataset, model or judge artifact, blog post, community engagement artifact, and two-page memo.

Detailed steps:

1. Open the challenge document and identify all Day 0 requirements.
2. Compare those requirements against `README.md`, `PRD.md`, `progress.md`, and `methodology.md`.
3. Record any mismatch between the challenge brief and current repo state.
4. Keep the existing Path B decision unless new Week 10 evidence contradicts it.
5. Add unresolved scope questions to the readiness review.

Done means:

```text
Day 0 scope is written down, Path B is still justified, and no one is planning a tau2-Bench retail rerun.
```

Status: Completed on 2026-04-27 after reviewing the challenge brief against `README.md`, `PRD.md`, `progress.md`, and `methodology.md`.

### 2. Lock The Path Declaration

- [x] Confirm Path B is the selected path.
- [x] Confirm ORPO is the selected preference-tuning algorithm.
- [x] Confirm the target component is a judge/critic, not a generation adapter.
- [x] Confirm the Week 10 evidence behind the decision is traceable.
- [x] Identify at least three Week 10 trace IDs that will support the final methodology rationale.
- [x] Identify at least two papers that will support the Path B rationale.

Detailed steps:

1. Review `progress.md` and `methodology.md`.
2. Pull supporting evidence from `seed/trace_log.jsonl`, `seed/held_out_traces.jsonl`, `seed/probe_library.md`, and `seed/failure_taxonomy.md`.
3. Mark candidate trace IDs for P33 gap-condescension and P24 AI-maturity empty JSON.
4. Confirm ORPO rationale: reference-free, single-stage, lower memory than DPO, practical on Colab T4.
5. Write a short Day 0 note in `progress.md` if any path assumption changes.

Done means:

```text
methodology.md contains a written Path B declaration with preliminary evidence and ORPO rationale.
```

Status: Completed on 2026-04-27.

Evidence confirmed:

- `methodology.md` declares Path B: preference-tuned judge / critic.
- `methodology.md` declares ORPO over DPO or SimPO because it is reference-free, single-stage, and practical for Colab T4.
- `seed/failure_taxonomy.md` identifies P24 AI maturity validity at 43.3% incident rate from tau2 thinking-model runs.
- `seed/failure_taxonomy.md` identifies P33 gap over-claiming and condescension at 15.6% incident rate from A/B signal-grounded outreach.
- `seed/probe_library.md` maps P24 to Tenacious-specific reframe T05: AI-maturity visibility.
- `seed/probe_library.md` maps P33 to high-business-risk condescension toward sophisticated buyers.

Candidate trace references for the final methodology rationale:

```text
P24 / AI-maturity empty JSON evidence:
- seed/held_out_traces.jsonl :: simulation_id=2ee84e7e-ebcb-4006-a066-1c9d373fc99f, task_id=1, reward=0.0
- seed/held_out_traces.jsonl :: simulation_id=d174d025-936f-49e7-8183-1497f8bac193, task_id=7, reward=0.0
- seed/held_out_traces.jsonl :: simulation_id=f5497551-5989-48a6-9c14-ac73106044ae, task_id=52, reward=0.0
- seed/held_out_traces.jsonl :: simulation_id=ba85025f-496d-43c0-91ed-39de2e2e480d, task_id=66, reward=0.0

P33 / gap-condescension evidence:
- seed/failure_taxonomy.md :: 5/32 signal-grounded A/B drafts rejected for layoff + AI-maturity + competitor-gap language.
- seed/probe_library.md :: P33 prospect CTO is ex-Google ML; gap brief recommends "adopt basic ML monitoring."
```

Path B papers queued:

```text
- Direct Preference Optimization, Rafailov et al.
- ORPO: Monolithic Preference Optimization without Reference Model, Hong, Lee, and Thorne.
- SimPO, Meng, Xia, and Chen, as comparison point.
- Preference Leakage, Li et al., for judge-training contamination controls.
```

### 3. Verify Accounts And Credentials

- [x] HuggingFace account exists.
- [x] HuggingFace write token exists.
- [x] HuggingFace token is available as `HUGGINGFACE_TOKEN` or `HF_TOKEN`.
- [x] OpenRouter account exists.
- [x] OpenRouter key is available as `OPENROUTER_API_KEY`.
- [x] Google Colab account can connect to a T4 runtime.
- [x] Optional RunPod fallback decision made; not required unless Colab caps become a risk.
- [x] No secrets are committed to git.

Detailed steps:

1. Create or sign in to HuggingFace.
2. Generate a write-scoped token for dataset and adapter publication.
3. Put the token in local environment config only, such as `.env`.
4. Create or sign in to OpenRouter.
5. Generate an API key and add it to local environment config.
6. Open Colab and start a T4 runtime at least once.
7. If using RunPod as fallback, verify account access and spending controls.
8. Confirm `.env` is ignored by git.

Done means:

```text
HuggingFace, OpenRouter, and Colab access are ready, and secrets remain outside version control.
```

### 4. Validate The Local Environment

- [x] Python 3.11+ is installed in the active `.venv`.
- [x] Virtual environment exists and can be activated.
- [x] Required packages can be installed from `requirements.txt`.
- [x] `transformers`, `peft`, `trl`, `datasets`, `accelerate`, and `bitsandbytes` import successfully.
- [x] The repo has a clear setup path in `README.md`.
- [x] The scoring command path is known: `python scoring/scoring_evaluator.py`.
- [x] Missing files such as `requirements.txt`, `.env.example`, or evaluator scripts are logged as blockers if absent.

Detailed steps:

1. Run `python --version`.
2. Create or activate `.venv`.
3. Install dependencies once `requirements.txt` exists.
4. Run:

```bash
python -c "import trl, peft; print(trl.__version__, peft.__version__)"
```

5. Confirm whether `scoring/scoring_evaluator.py` exists yet.
6. If the evaluator does not exist, add it to Day 1 work as an Act I blocker.
7. Confirm local commands in `README.md` match actual file locations.

Done means:

```text
The local environment is either verified or every missing setup artifact is named in the Day 1 blocker list.
```

Step 4 verification:

- `requirements.txt` exists.
- `.env.example` exists without secrets.
- `python scoring/scoring_evaluator.py` runs and returns passing numeric smoke scores.

### 5. Inventory Week 10 Seed Artifacts

- [x] `seed/trace_log.jsonl` exists.
- [x] `seed/probe_library.md` exists.
- [x] `seed/failure_taxonomy.md` exists.
- [x] `seed/held_out_traces.jsonl` exists.
- [x] Files are parseable or readable.
- [x] At least eight probe IDs are identified for the Day 1 audit memo.
- [x] At least five trace examples are identified for the Day 1 audit memo.
- [x] Candidate rejected/chosen examples for Path B preference data are flagged.

Detailed steps:

1. Check that each seed file exists and has non-zero size.
2. Sample `trace_log.jsonl` and `held_out_traces.jsonl` for valid JSONL structure.
3. Extract probe IDs from `probe_library.md`.
4. Extract measured failure categories from `failure_taxonomy.md`.
5. Create a working notes list:

```text
Trace ID:
Failure mode:
Why diagnostic:
Possible benchmark dimension:
Potential chosen/rejected pair:
```

6. Prioritize P33 and P24 because the current methodology declares them as the strongest Path B evidence.

Done means:

```text
Week 10 materials are confirmed present and enough trace/probe evidence is queued for Act I.
```

Step 5 verification:

- `seed/trace_log.jsonl`: 150 parseable JSONL records; 109 reward=1.0, 41 reward=0.0.
- `seed/held_out_traces.jsonl`: 17 parseable JSONL records; 9 reward=1.0, 8 reward=0.0.
- Working notes created in `seed/day1_seed_inventory.md`.

### 6. Review The Schema Starter And Day 1 Build Targets

- [x] Confirm whether a schema starter exists.
- [x] Confirm `schema.json` exists or create it on Day 1.
- [x] Confirm three dummy tasks are required for Act I.
- [x] Confirm the evaluator must score a task plus candidate output with no human in the loop.
- [x] Confirm each task needs metadata for source mode, partition, difficulty, and failure dimension.
- [x] Confirm scoring dimensions are machine-verifiable wherever possible.

Detailed steps:

1. Search the repo for `schema.json`.
2. If missing, add it to the Day 1 task queue.
3. Define initial task fields:

```text
task_id
partition
source_mode
difficulty
failure_dimension
input
candidate_output
ground_truth
rubric
scoring_config
metadata
```

4. Define initial Path B scoring targets:

```text
gap_condescension
ai_maturity_consistency
signal_grounding
style_guide_adherence
output_validity
next_step_quality
```

Current Day Zero deterministic smoke checks use narrower names:

```text
output_nonempty
ai_maturity_keyword_present
banned_condescension_absent
expected_signal_term_present
forbidden_terms_absent
buyer_next_step_keyword_present
```

5. Confirm the Day 1 evaluator can score three hand-built dummy tasks before any large dataset generation.

Done means:

```text
The schema/evaluator requirements are clear enough to implement Act I without re-reading the challenge brief.
```

Step 6 verification:

- `schema.json` exists at the repo root.
- `tenacious_bench_v0.1/dev/dummy_tasks.jsonl` contains three valid dummy tasks.
- All three dummy tasks validate against `schema.json` and receive passing numeric evaluator scores.

### 7. Run Or Schedule The Unsloth Smoke Test

- [x] Colab T4 runtime can start.
- [x] Unsloth notebook path is known.
- [x] Dummy five-task LoRA run is planned.
- [x] Adapter push to HuggingFace is tested or scheduled.
- [x] Expected first-run compile time of 6-10 minutes is accounted for.
- [x] Precision choice is documented: fp16 on Colab T4, bf16 on RunPod 4090 or Colab Pro L4.
- [x] QLoRA 4-bit is not selected unless the training plan is explicitly revised.

Detailed steps:

1. Open the Unsloth Qwen3 fine-tuning guide.
2. Create a five-example dummy preference dataset for ORPO.
3. Run the notebook on Colab T4.
4. Confirm the training cell completes.
5. Push a test adapter to a private or disposable HuggingFace repo if possible.
6. Record compile time, runtime, package versions, and any error messages.
7. If the smoke test fails, capture the exact blocker for Day 1.

Done means:

```text
The training environment is proven viable, or the exact compute blocker is known before Day 5.
```

Step 7 verification:

- Colab T4 access was confirmed with `nvidia-smi`.
- Unsloth Qwen3 guide and general fine-tuning guide were checked.
- Smoke-test plan created in `training/unsloth_smoke_test_plan.md`.
- Five-record dummy ORPO preference dataset created in `training/dummy_orpo_preferences.jsonl`.
- Actual Colab training run and adapter push are scheduled manual actions.

### 8. Set Up Cost Tracking

- [x] `cost_log.csv` exists or is queued for creation.
- [x] Budget cap is set at USD 10.
- [x] Dataset authoring budget is capped at USD 3-5.
- [x] Training budget is capped at USD 0-5.
- [x] Held-out evaluation budget is capped at USD 2-3.
- [x] Reserve budget is capped at USD 1-2.
- [x] No eval-tier model calls are planned for Days 2-3.
- [x] Every API or compute charge has timestamp, bucket, model/provider, purpose, and amount.

Detailed steps:

1. Create a cost log with these columns:

```text
timestamp_utc,bucket,provider,model_or_compute,purpose,estimated_cost_usd,actual_cost_usd,notes
```

2. Add starting budget rows for each bucket.
3. Add a rule in project notes: no tau2-Bench retail reruns.
4. Add a rule in project notes: no eval-tier authoring or dedup on Days 2-3.
5. Add one row for every smoke test, synthesis call, judge call, training run, and held-out pass.

Done means:

```text
The project can prove cost discipline, not merely claim it.
```

Step 8 verification:

- `cost_log.csv` exists with the required columns and starting budget rows.
- `cost_controls.md` documents the USD 10 cap, bucket limits, no tau2-Bench retail reruns, and no eval-tier authoring/dedup on Days 2-3.
- Starting budget rows sum to USD 10.

### 9. Draft The First Common Reading Memo

- [x] Select one common reading to complete on Day 0.
- [x] Draft a one-page synthesis memo in `synthesis_memos/`.
- [x] Include one design choice from the paper that applies to Tenacious-Bench.
- [x] Include one specific disagreement or limitation.
- [x] Tie the memo to a concrete repo decision.

Recommended Day 0 reading:

```text
Best Practices and Lessons Learned on Synthetic Data for Language Models
```

Why this first:

```text
It directly informs Days 2-3 dataset authoring, which the challenge identifies as the hardest engineering problem of the week.
```

Detailed steps:

1. Read the paper with the dataset construction pipeline in mind.
2. Extract guidance for synthetic task generation, filtering, and quality thresholds.
3. Write the memo with this structure:

```text
Claim I will use:
Design choice it changes:
Where I disagree:
Evidence I will collect:
Repo artifact affected:
```

4. Commit the draft as v0 if it is not yet polished.

Done means:

```text
At least one common-reading memo exists and informs the Act II dataset construction plan.
```

Step 9 verification:

- Common reading selected: Liu et al., "Best Practices and Lessons Learned on Synthetic Data".
- Memo drafted at `synthesis_memos/synthetic_data_best_practices_v0.md`.
- Memo ties the paper to controlled synthesis, provenance-heavy schema design, filtering,
  contamination checks, and model-family rotation.

### 10. Prepare The Day 1 Work Queue

- [ ] Create or confirm `audit_memo.md`.
- [ ] Create or confirm `schema.json`.
- [ ] Create or confirm `scoring/scoring_evaluator.py`.
- [ ] Prepare three dummy tasks.
- [ ] Prepare a probe/trace evidence list for the audit memo.
- [ ] Identify exact benchmark gaps that public retail benchmarks miss.
- [ ] Confirm Act I acceptance criteria.

Detailed steps:

1. Convert the Day 0 artifact inventory into Day 1 tasks.
2. Keep Day 1 focused on audit and schema design.
3. Write acceptance criteria for each task:

```text
audit_memo.md: max 600 words, cites at least eight probe IDs and five trace examples.
schema.json: validates three example tasks.
scoring_evaluator.py: returns numerical scores for three dummy tasks without human input.
methodology.md: includes path declaration and preliminary evidence.
```

4. Put anything not required for Act I into a later-act backlog.

Done means:

```text
Day 1 starts with an ordered execution queue, not a vague goal.
```

## Day Zero Readiness Review

Use this final checklist at the end of Day 0.

- [ ] Challenge brief requirements reviewed.
- [ ] Path B and ORPO decision confirmed.
- [x] HuggingFace account and token ready.
- [x] OpenRouter account and key ready.
- [x] Colab T4 runtime tested.
- [x] Optional RunPod fallback decision made.
- [x] Local Python environment verified or blockers listed.
- [x] Week 10 seed artifacts confirmed present.
- [x] Candidate trace IDs and probe IDs identified.
- [x] Schema/evaluator Day 1 requirements clear.
- [x] Unsloth smoke test completed or scheduled with blocker notes.
- [x] Cost log created.
- [x] First common-reading memo drafted or assigned to the next immediate work block.
- [ ] Day 1 work queue prepared.

## Day 1 Immediate Next Actions

1. Write `audit_memo.md` using Week 10 probe and trace evidence.
2. Implement `schema.json` with three example tasks.
3. Implement `scoring/scoring_evaluator.py` for deterministic checks plus judge-ready scoring hooks.
4. Update `methodology.md` with exact trace IDs and paper references.
5. Add `requirements.txt` and `.env.example`, then create a Python 3.11+ `.venv`.
6. Prepare the first dataset-authoring scripts for trace-derived and programmatic tasks.

## Risks To Watch

| Risk | Impact | Day Zero mitigation |
|---|---|---|
| Missing API keys | Blocks synthesis, judge filtering, and publication | Verify HuggingFace and OpenRouter keys today |
| Colab/Unsloth failure | Delays Day 5 training | Run dummy LoRA smoke test today |
| Weak trace evidence | Weakens audit and path rationale | Inventory at least five traces and eight probes today |
| Vague rubric | Prevents machine-verifiable benchmark | Force Day 1 schema to score three dummy tasks |
| Budget drift | Fails cost-discipline observable | Create cost log before first paid call |
| Preference leakage | Invalidates Path B judge training | Maintain generate/judge model-family rotation from the start |

## Definition Of Done

Day Zero is complete when:

```text
Access works, compute is proven or blocked with specifics, seed artifacts are inventoried,
Path B is justified, cost tracking is live, the first reading memo exists or is queued, and
Day 1 can begin with audit/schema/evaluator implementation.
```
