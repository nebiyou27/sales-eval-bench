# Methodology — Tenacious-Bench v0.1

## Path Declaration

**Path B — Preference-tuned judge / critic**

### Justification

Week 10 evidence points to two dominant failure modes:

1. **P33 — Gap-condescension** (15.6% trigger rate, A/B n=32 signal-grounded drafts): the
   agent generates an output but cannot detect when its language is presumptuous or intrusive
   toward sophisticated buyers. The sensitivity axis in `agent/claims/sensitivity.py` flags the
   claim kind but does not prevent the generation from proceeding with inappropriate confidence.
   Trace reference: `eval/ab_reply_rate_report.json` — 5/32 signal-grounded drafts rejected by
   judge for layoff + AI-maturity + competitor-gap language.

2. **P24 — AI maturity empty JSON** (43.3% incident rate, tau2 n=30 thinking-model tasks): the
   agent produces empty or invalid JSON on hard AI-maturity tasks and cannot self-identify the
   failure. The system scores it as a pass internally while the output is unusable.
   Trace reference: `deliverables/held_out_traces.jsonl`, task IDs from tau2 dev-slice run
   `conversion_engine_treatment`.

Both are **inconsistency failures**: the agent is right most of the time but has no mechanism
to catch when it is wrong. A trained judge/critic (Path B) is the correct treatment. A
generation fix (Path A) would only improve average output quality; it would not add
self-detection. A PRM (Path C) requires multi-turn trajectory data we do not have at scale.

### Algorithm choice

**ORPO** (Hong, Lee, and Thorne, EMNLP 2024) over DPO or SimPO.

Rationale: ORPO is reference-free (no separate reference model required), trains in a single
stage, and has been shown to match or outperform DPO at lower memory cost — critical for Colab
T4 (16 GB VRAM). SimPO is also reference-free but requires a length-normalization term that
complicates calibration on short sales-outreach outputs. DPO requires a reference model pass
that doubles VRAM use on T4.

---

## Partitioning Protocol

| Partition | Share | Size (target) | Use |
|---|---|---|---|
| `train/` | 50% | ~125 tasks | LoRA training |
| `dev/` | 30% | ~75 tasks | Iteration, rubric calibration |
| `held_out/` | 20% | ~50 tasks | Sealed evaluation only |

Held-out is sealed after contamination checks pass. It is gitignored from training scripts and
not committed in unencrypted form until the leaderboard is published.

---

## Contamination Protocol

Three checks before any task enters the held-out partition:

1. **N-gram overlap** — less than 8-gram overlap on input fields between held-out and training.
2. **Embedding similarity** — cosine similarity below 0.85 between held-out and training tasks
   using `all-MiniLM-L6-v2`.
3. **Time-shift verification** — any task referencing public signal (layoffs, job posts, funding)
   must cite a documentable retrieval window, not a generic placeholder.

Results committed to `generation_scripts/contamination_check.json`.

---

## Multi-LLM Routing Policy

To prevent preference leakage (Li et al., 2025), model families are rotated:

| Role | Model | Budget tier |
|---|---|---|
| Hard-seed authoring (30–50 seeds) | Claude Sonnet 4.6 | eval-tier, Days 4–6 only |
| Bulk variation generation | Qwen3-Next-80B via OpenRouter | dev-tier |
| Judge filtering (quality scores) | DeepSeek V3.2 via OpenRouter | dev-tier |
| Calibration spot-check (50 tasks) | Claude Sonnet 4.6 | eval-tier |
| Chosen-rewrite for preference pairs | Qwen3-Next-80B | dev-tier (different family from judge) |

The same model is never used to generate and judge the same task.

---

## Inter-Rater Agreement

30-task subset hand-labeled against rubric, then re-labeled 24 hours later without reference
to first labels. Agreement matrix committed to `inter_rater_agreement.md`.

Threshold: ≥80% agreement on each rubric dimension before the held-out is sealed.
