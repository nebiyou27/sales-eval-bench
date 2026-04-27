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
# Validate schema
python scoring/scoring_evaluator.py

# Author dataset (Days 2-3)
python generation_scripts/generate_programmatic.py
python generation_scripts/generate_synthesis.py

# Run contamination checks
python generation_scripts/contamination_check.py

# Training (Day 5)
# See training/README.md
```

## Directory Index

| Path | Purpose |
|---|---|
| `tenacious_bench_v0.1/` | Dataset partitions (train/dev/held_out) |
| `generation_scripts/` | Authoring pipeline (programmatic, synthesis, dedup, judge filter) |
| `scoring/` | Machine-verifiable scoring evaluator |
| `training/` | LoRA training script and hyperparameters |
| `ablations/` | Ablation results and held-out traces |
| `synthesis_memos/` | Paper reading memos |
| `seed/` | Week 10 artifacts used as inputs |

## Key files

- `audit_memo.md` — what τ²-Bench misses for Tenacious-specific work
- `schema.json` — Tenacious-Bench task schema
- `methodology.md` — path declaration, partitioning, contamination protocol
- `datasheet.md` — Gebru + Pushkarna documentation
