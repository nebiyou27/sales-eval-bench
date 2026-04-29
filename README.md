# Tenacious-Bench: Sales Agent Evaluation Bench

TRP1 Week 11 — Nebiyou Abebe (nebiyoua@10academy.org)

A Tenacious-specific evaluation benchmark and trained judge for the Week 10 Conversion Engine.

## Status

Acts I–II in progress.

## What this is

A 200–300 task evaluation dataset covering Tenacious-specific sales agent failure modes, plus a trained LoRA judge (Path B — preference-tuned critic) that catches gap-condescension and AI-maturity inconsistency failures.

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
python src/generation/generate_synthesis.py

# Run contamination checks
python src/generation/contamination_check.py

# Training (Day 5) — see docs/training/unsloth_smoke_test_plan.md
```

## Directory Index

| Path | Purpose |
|---|---|
| `tenacious_bench_v0.1/` | Dataset partitions (`train/`, `dev/`, `held_out/`) and `smoke/` fixtures |
| `seed/` | Read-only Week 10 inputs (traces, probes, taxonomy) |
| `src/generation/` | Authoring pipeline (programmatic, synthesis, dedup, judge filter) |
| `src/scoring/` | Machine-verifiable scoring evaluator |
| `src/training/` | LoRA training scripts and hyperparameters |
| `src/ablations/` | Ablation runners |
| `tests/` | Unit tests |
| `docs/` | Project documentation (PRD, methodology, progress, audit memo, plans, memos) |
| `cost/` | Cost log (`log.csv`, gitignored) |

## Key files

- `schema.json` — Tenacious-Bench task schema
- `docs/methodology.md` — path declaration, partitioning, contamination protocol
- `docs/PRD.md` — acceptance criteria
- `docs/progress.md` — decision log
- `docs/audit_memo.md` — what τ²-Bench misses for Tenacious-specific work
