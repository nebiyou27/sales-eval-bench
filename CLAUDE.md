# CLAUDE.md — Sales Eval Bench (TRP1 Week 11)

Read this fully before every response.

---

## 1. Project Context

**What this is:** A Tenacious-specific evaluation benchmark (Tenacious-Bench v0.1) plus a trained
LoRA judge (Path B — ORPO preference-tuned critic) that catches the two dominant Week 10 failure
modes: gap-condescension (P33, 15.6%) and AI-maturity inconsistency (P24, 43.3%).

**The real challenge:** Building a machine-verifiable benchmark from a thin seed corpus. The
training run is 30–90 minutes. The dataset is the hard part.

**Week 10 system:** `D:\TRP-1\week-10\Conversion Engine` — the Conversion Engine whose failures
are being benchmarked. All seed artifacts live in `seed/`.

### Deadlines
- **Wed Apr 30, 21:00 UTC** — Acts I + II (audit, schema, dataset)
- **Sat May 3, 21:00 UTC** — Acts III–V (training, ablations, public artifacts)

---

## 2. Architecture

```
SEED (Week 10 traces/probes)
    ↓
DATASET AUTHORING (4 modes: trace-derived, programmatic, synthesis, hand-authored)
    ↓ LLM-as-judge filter
TENACIOUS-BENCH v0.1 (train 50% / dev 30% / held_out 20%)
    ↓ contamination checks
TRAINING (ORPO LoRA on Qwen3-0.6B, fallback Qwen3-1.7B, Unsloth, Colab T4)
    ↓
ABLATIONS (Delta A on held-out, Delta B vs prompt-only, cost-Pareto)
    ↓
PUBLIC ARTIFACTS (HuggingFace dataset + model, blog post, community engagement)
```

---

## 3. Folder Structure

```
Sales Eval Bench/
├── CLAUDE.md                    # This file
├── PRD.md                       # Acceptance criteria
├── README.md
├── progress.md                  # Decision log
├── methodology.md               # Path B declaration, partitioning, contamination protocol
├── audit_memo.md                # Act I — what τ²-Bench misses
├── schema.json                  # Tenacious-Bench task schema
├── datasheet.md                 # Gebru + Pushkarna documentation
├── inter_rater_agreement.md     # Agreement matrix
│
├── seed/                        # Week 10 artifacts (read-only inputs)
│   ├── trace_log.jsonl
│   ├── probe_library.md
│   ├── failure_taxonomy.md
│   └── held_out_traces.jsonl
│
├── tenacious_bench_v0.1/
│   ├── train/                   # 50% — LoRA training data
│   ├── dev/                     # 30% — iteration and rubric calibration
│   └── held_out/                # 20% — sealed, gitignored
│
├── generation_scripts/          # Authoring pipeline
│   ├── generate_programmatic.py
│   ├── generate_synthesis.py
│   ├── judge_filter.py
│   ├── dedup.py
│   └── contamination_check.py
│
├── scoring/
│   └── scoring_evaluator.py     # Machine-verifiable scorer
│
├── training/
│   ├── prepare_orpo_data.py
│   ├── train_orpo.py
│   └── training_run.log
│
├── ablations/
│   ├── ablation_results.json
│   └── held_out_traces.jsonl
│
└── synthesis_memos/             # Paper reading memos (one per paper)
```

---

## 4. Rules

### R1 — Machine-Verifiable Rubric
Every rubric dimension must be scoreable by a script without human input. "Sounds on-brand" is
not a rubric. "Zero banned phrases AND ≥1 signal citation AND ≥4/5 on tone judge" is.

### R2 — No Preference Leakage
Never use the same model family to generate and judge the same task. Rotation policy is in
`methodology.md`.

### R3 — Held-Out Is Sacred
Nothing from held_out/ enters training. Contamination checks run before sealing. Held-out is
gitignored and not committed unencrypted.

### R4 — Cost Discipline
Total budget: $10. Dev-tier models (Qwen3-Next, DeepSeek V3.2) on Days 2–3. Eval-tier
(Claude Sonnet 4.6) only on Days 4–6 for spot-check and ablation. No τ²-Bench re-runs.
Every charge logged in cost_log.csv with timestamp + bucket + purpose.

### R5 — Path B Evidence
Every design choice in training cites at least one of: P33 trace ID, P24 trace ID, or a
specific section from a required paper. Methodology without evidence is a grading failure.

### R6 — Simplicity First
No features beyond what was asked. No abstractions for single-use code. Match existing style.

---

## 5. Training Path

**Path B — ORPO preference-tuned judge/critic**

Backbone: Qwen3-0.6B for the first smoke run; Qwen3-1.7B only if T4 memory and runtime are stable.
Python dependencies are pinned in `requirements.txt`; re-pin only if the Day 5 Colab/Unsloth
runtime requires a compatible training stack.
Algorithm: ORPO (reference-free, single-stage, fits T4 16 GB VRAM)
Framework: Unsloth + HuggingFace TRL
Compute: Google Colab T4 (free)

Preference pairs:
- rejected = probe-triggered failure outputs (P33/P24 instances from trace_log.jsonl)
- chosen = corrected outputs (hand-fixes + Qwen3-Next rewrites that pass scoring_evaluator)
- judge for chosen-rewrites = DeepSeek V3.2 (different family from generation model)

---

## 6. Session Resume Protocol

> "Read CLAUDE.md, PRD.md, README.md, and progress.md in order. Confirm understanding and
> tell me where we left off."

---

## 7. User Profile

- Nebiyou Abebe (nebiyoua@10academy.org) — 10 Academy trainee, TRP1
- Built Week 10 Conversion Engine with epistemic layering, probe library, A/B eval
- Familiar with probe/eval methodology, systems thinking framing
- Prefers plain-English answers, dislikes document summaries
- Presents on Slack and standups
