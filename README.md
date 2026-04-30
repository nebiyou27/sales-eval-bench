# Tenacious-Bench: Sales Agent Evaluation Bench

TRP1 Week 11 - Nebiyou Abebe (nebiyoua@10academy.org)

A Tenacious-specific evaluation benchmark and trained judge for the Week 10 Conversion Engine.

## Status

Acts I-II are implemented in repo form. Current validated corpus in this workspace: `train/` has
132 tasks, `dev/` has 79 tasks, and local sealed `held_out/` has 50 tasks for a total of 261
benchmark rows. All 4
authoring modes have runnable code paths, including live synthetic generation with judge rotation,
seed stamping, and duplicate filtering.

The local `held_out/` slice now reaches the 50-task target and passes the contamination gate. It
remains gitignored and sealed from training use, and `src/training/prepare_orpo_data.py` now
indexes only `train/` and `dev/` when preparing preference data.

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
```

`contamination_check.py` now prefers a repo-local MiniLM snapshot at
`models/embeddings/all-MiniLM-L6-v2/`. Use `src/generation/fetch_embedding_model.py` once to
bootstrap that cache, then rerun contamination to get a true embedding-backed pass.

## Directory Index

| Path | Purpose |
|---|---|
| `tenacious_bench_v0.1/` | Dataset partitions (`train/`, `dev/`, `held_out/`) and `smoke/` fixtures |
| `seed/` | Read-only Week 10 inputs (traces, probes, taxonomy) |
| `src/generation/` | Authoring pipeline (trace-derived, programmatic, hand-authored, synthesis, contamination) |
| `src/scoring/` | Machine-verifiable scoring evaluator |
| `src/training/` | LoRA training scripts and hyperparameters |
| `src/ablations/` | Ablation runners |
| `tests/` | Unit tests |
| `docs/` | Project documentation (PRD, methodology, progress, audit memo, plans, memos) |
| `cost/` | Cost log (`log.csv`, gitignored) |

## Key files

- `schema.json` - Tenacious-Bench task schema
- `docs/methodology.md` - path declaration, partitioning, contamination protocol
- `docs/PRD.md` - acceptance criteria
- `docs/progress.md` - decision log
- `docs/audit_memo.md` - what tau2-Bench misses for Tenacious-specific work
- `docs/datasheet.md` - Gebru-style datasheet with layered corpus details
- `docs/memos/` - synthesis decision memos for synthetic-data policy and judge rotation

## Forward plan

The current repo is strong enough for audit, scoring, controlled synthesis work, and a sealed
held-out evaluation pass. The next two steps remain:

1. Convert the accepted benchmark rows into a richer ORPO preference corpus with explicit
   chosen/rejected pairs, then run the first end-to-end Unsloth smoke training pass.
2. Complete the pending human-reliability work in `docs/inter_rater_agreement.md` before making
   stronger ablation or benchmark-calibration claims in Act III.

The next quality upgrades are intentionally quantitative:

- add more synthetic tasks in under-covered regions, especially `sms`, `next_step_quality`, and
  `signal_grounding`,
- report per-dimension acceptance and rejection counts for live synthesis,
- log preference-prep drop rates and rotation-policy rejections,
- add human agreement results once the second pass and second-labeler review are complete.

## External references

Project decisions in this repo are grounded in a small set of external references:

- Gebru et al., "Datasheets for Datasets" - framing for [docs/datasheet.md](docs/datasheet.md)
- Pushkarna et al. dataset documentation guidance - layered dataset documentation style used in
  the datasheet
- Hong, Lee, and Thorne, "ORPO: Monolithic Preference Optimization without Reference Model" -
  training choice for Path B
- Liu et al., "Best Practices and Lessons Learned on Synthetic Data" - basis for
  [docs/memos/synthetic_data_best_practices_v0.md](docs/memos/synthetic_data_best_practices_v0.md)
- the project memo on judge rotation and leakage control in
  [docs/memos/judge_rotation_and_preference_leakage_v0.md](docs/memos/judge_rotation_and_preference_leakage_v0.md)

For repo-local evidence and rationale, start with:

- [docs/audit_memo.md](docs/audit_memo.md)
- [docs/methodology.md](docs/methodology.md)
- [docs/datasheet.md](docs/datasheet.md)
- [docs/progress.md](docs/progress.md)
