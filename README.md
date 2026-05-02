# Tenacious-Bench: Sales Agent Evaluation Bench

TRP1 Week 11 - Nebiyou Abebe (nebiyoua@10academy.org)

A Tenacious-specific evaluation benchmark and trained judge for the Week 10 Conversion Engine.

## Public Artifacts

| Artifact | URL |
|---|---|
| HuggingFace dataset | https://huggingface.co/datasets/nebiyoua/tenacious-bench-v0.1 |
| HuggingFace model (LoRA adapter) | https://huggingface.co/nebiyoua/tenacious-bench-orpo-qwen25-0_5b-lora |
| Blog post | https://nebiyoua.github.io/tenacious-bench-orpo-write-up/ |
| Community engagement | https://github.com/nebiyou-abebe/tenacious-bench/issues/1 |

These URLs are reserved for the Sat May 3 release. Replace with the live links once each artifact
is published.

## Status

Acts I-II are implemented in repo form. Current validated corpus in this workspace: `train/` has
132 tasks, `dev/` has 79 tasks, and local sealed `held_out/` has 50 tasks for a total of 261
benchmark rows. All 4
authoring modes have runnable code paths, including live synthetic generation with judge rotation,
seed stamping, and duplicate filtering.

The local `held_out/` slice now reaches the 50-task target and passes the contamination gate. It
remains gitignored and sealed from training use, and `src/training/prepare_orpo_data.py` now
indexes only `train/` and `dev/` when preparing preference data. Human inter-rater agreement is
still pending, so the corpus should not yet be described as fully human-calibrated. The committed
repo includes the held-out generators, tests, documentation, and contamination report, but not the
held-out task rows themselves.

## Current counts

| field | values |
|---|---|
| `partition` | `train` 132, `dev` 79, `held_out` 50, `total` 261 |
| `source_mode` | `programmatic` 123, `trace_derived` 60, `hand_authored` 67, `synthetic` 11 |
| `failure_dimension` | `gap_condescension` 51, `ai_maturity_consistency` 51, `signal_grounding` 44, `style_guide_adherence` 41, `output_validity` 38, `next_step_quality` 36 |
| `difficulty` | `hard` 132, `medium` 71, `easy` 58 |
| `channel` | `email` 182, `linkedin_dm` 70, `sms` 9 |

## What this is

A 200-300 task evaluation dataset covering Tenacious-specific sales agent failure modes, plus a
trained LoRA judge (Path B - preference-tuned critic) that catches gap-condescension and
AI-maturity inconsistency failures.

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
cp .env.example .env
# fill in OPENROUTER_API_KEY, HUGGINGFACE_TOKEN
```

## Run order

```bash
# Validate evaluator smoke
python src/scoring/scoring_evaluator.py

# Author dataset (Days 2-3)
python src/generation/generate_trace_derived.py
python src/generation/generate_programmatic.py
python src/generation/generate_hand_authored.py --partition train
python src/generation/generate_hand_authored.py --partition held_out
python src/generation/generate_synthesis.py --seed 11
# optional live synthesis with judge rotation enforced in code
python src/generation/generate_synthesis.py --live --judge-model deepseek/deepseek-chat --seed 11

# Run contamination checks
python src/generation/fetch_embedding_model.py
python src/generation/contamination_check.py

# Training (Day 5) - see docs/training/unsloth_smoke_test_plan.md
python src/training/train_orpo.py --dry-run

# Ablations (Act IV)
python src/ablations/run_ablation.py --comparison all --baseline-predictions path\\to\\baseline.jsonl --trained-predictions path\\to\\trained.jsonl --prompt-only-predictions path\\to\\prompt_only.jsonl

# Judge filter pipeline
python src/generation/judge_filter.py --input tenacious_bench_v0.1\\train\\synthetic_tasks.jsonl --output tenacious_bench_v0.1\\train\\synthetic_tasks_filtered.jsonl
```

`contamination_check.py` now prefers a repo-local MiniLM snapshot at
`models/embeddings/all-MiniLM-L6-v2/`. Use `src/generation/fetch_embedding_model.py` once to
bootstrap that cache, then rerun contamination to get a true embedding-backed pass.

## Directory Index

| Path | Purpose |
|---|---|
| `configs/` | Future home for stabilized run presets and externalized configuration |
| `reports/` | Generated reports and reproducible run summaries |
| `tenacious_bench_v0.1/` | Public dataset partitions (`train/`, `dev/`), local sealed `held_out/`, and `smoke/` fixtures |
| `seed/` | Read-only Week 10 inputs (traces, probes, taxonomy) |
| `src/generation/` | Authoring pipeline (trace-derived, programmatic, hand-authored, synthesis, contamination) |
| `src/scoring/` | Machine-verifiable scoring evaluator |
| `src/training/` | LoRA training scripts and hyperparameters |
| `src/ablations/` | Ablation runners |
| `tests/` | Unit tests |
| `docs/` | Project documentation (PRD, methodology, progress, architecture, audit memo, plans, memos) |
| `cost/` | Cost log (`log.csv`, gitignored) |

## Architecture Notes

The folder structure is now intentionally split by system concern rather than by day-of-week work:

- evidence inputs live in `seed/`
- benchmark data lives in `tenacious_bench_v0.1/`
- executable logic lives in `src/`
- authored governance and methodology live in `docs/`
- generated run outputs belong in `reports/`

That separation keeps provenance, code, and reproducible artifacts from drifting together as the
repo grows.

## Key files

- `schema.json` - Tenacious-Bench task schema
- `methodology.md` - path declaration, partitioning, contamination protocol
- `methodology_rationale.md` - Path B justification with trace IDs and paper anchors
- `audit_memo.md` - what tau2-Bench misses for Tenacious-specific work
- `datasheet.md` - Gebru-style datasheet with layered corpus details
- `inter_rater_agreement.md` - protocol, agreement matrices, final agreement
- `docs/PRD.md` - acceptance criteria
- `docs/progress.md` - decision log
- `docs/INDEX.md` - documentation map
- `docs/memos/` - synthesis decision memos for synthetic-data policy and judge rotation
- `src/generation/judge_filter.py` - pointwise + pairwise synthetic admission filter with calibration sampling
- `src/training/train_orpo.py` - explicit ORPO/LoRA training entrypoint
- `src/ablations/run_ablation.py` - shared Delta A / Delta B / Delta C / Cost-Pareto harness

## Forward plan

The current repo is strong enough for audit, scoring, controlled synthesis work, and a sealed
held-out evaluation pass. The human-reliability caveat remains explicit: second-pass and
second-labeler agreement are still pending. The next two steps remain:

1. Convert the accepted benchmark rows into a richer ORPO preference corpus with explicit
   chosen/rejected pairs, then run the first end-to-end Unsloth smoke training pass.
2. Publish the public artifacts (HuggingFace dataset, blog post, community engagement link) and
   wire the headline Delta A number from the held-out evaluation back into this README.

The next quality upgrades are intentionally quantitative:

- add more synthetic tasks in under-covered regions, especially `sms`, `next_step_quality`, and
  `signal_grounding`,
- report per-dimension acceptance and rejection counts for live synthesis,
- log preference-prep drop rates and rotation-policy rejections,
- add human agreement results once the second pass and second-labeler review are complete.

## Attribution

Built for 10 Academy TRP1 Week 11 using Week 10 Tenacious evaluation evidence, public dataset
documentation guidance from Gebru et al., synthetic-data controls from Liu et al., and ORPO
training methodology from Hong, Lee, and Thorne.

## Known caveats before training

- Human inter-rater agreement is complete on the 30-task subset; both test-retest and
  inter-rater passes clear the 80% threshold post one rubric revision (`ai_maturity_consistency`).
  See `inter_rater_agreement.md` for matrices and Wilson 95% CIs.
- Synthetic coverage is 11 tasks, which is below the original target mix, so the current corpus
  remains programmatic and trace-heavy.
- `cost/log.csv` records live usage events, but actual-cost reconciliation is still pending until a
  provider usage export is available. Current `0.00` actual-cost entries should not be treated as a
  final cost claim.

## External references

Project decisions in this repo are grounded in a small set of external references:

- Gebru et al., "Datasheets for Datasets" - framing for [datasheet.md](datasheet.md)
- Pushkarna et al. dataset documentation guidance - layered dataset documentation style used in
  the datasheet
- Hong, Lee, and Thorne, "ORPO: Monolithic Preference Optimization without Reference Model" -
  training choice for Path B
- Liu et al., "Best Practices and Lessons Learned on Synthetic Data" - basis for
  [docs/memos/synthetic_data_best_practices_v0.md](docs/memos/synthetic_data_best_practices_v0.md)
- the project memo on judge rotation and leakage control in
  [docs/memos/judge_rotation_and_preference_leakage_v0.md](docs/memos/judge_rotation_and_preference_leakage_v0.md)

For repo-local evidence and rationale, start with:

- [audit_memo.md](audit_memo.md)
- [methodology.md](methodology.md)
- [methodology_rationale.md](methodology_rationale.md)
- [datasheet.md](datasheet.md)
- [inter_rater_agreement.md](inter_rater_agreement.md)
- [docs/progress.md](docs/progress.md)
