# Tenacious-Bench: Sales Agent Evaluation Bench

TRP1 Week 11 - Nebiyou Abebe (nebiyoua@10academy.org)

A Tenacious-specific evaluation benchmark and trained judge for the Week 10 Conversion Engine.

## Status

Acts I-II are implemented in repo form. Current committed corpus: `train/` has 132 tasks, `dev/`
has 79 tasks, and `held_out/` has 14 sealed tasks. All 4 authoring modes have runnable code
paths, including live synthetic generation with judge rotation, seed stamping, and duplicate
filtering.

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
