# Tenacious-Bench v0.1: A Sales Outreach Eval Benchmark

**Nebiyou Abebe · May 2026 · [Dataset on HuggingFace](https://huggingface.co/datasets/Nebiyou21/tenacious-bench-v0.1)**

---

## What This Is

Tenacious-Bench v0.1 is a machine-verifiable evaluation benchmark for AI-assisted B2B sales
outreach, built to catch the two dominant failure modes identified in the Week 10 Conversion
Engine audit:

| Failure Mode | Probe ID | Observed Rate |
|---|---|---|
| Gap-condescension — agent implies the prospect is behind | P33 | 15.6% |
| AI-maturity inconsistency — contradicts confidence signal mid-email | P24 | 43.3% |

The benchmark contains **211 ORPO preference pairs** and **211 task examples** across four
authoring modes: trace-derived, programmatic, synthetic, and hand-authored.

---

## Approach: Path B — ORPO Preference-Tuned Critic

Rather than prompt engineering, I trained a LoRA adapter on top of Qwen3-0.6B using ORPO
(odds-ratio preference optimization) — a reference-free, single-stage algorithm that fits a
T4 GPU (16 GB VRAM).

**Preference pair construction:**
- **Rejected:** probe-triggered failure outputs sourced from `trace_log.jsonl` (P33/P24 instances)
- **Chosen:** corrected outputs — hand-fixed or rewritten by Qwen3-Next, judged by DeepSeek V3.2
- **No model family overlap** between generation and judgment (R2 — no preference leakage)

**Rubric design principle:** Every dimension is scoreable by a script. "Sounds professional" is
not a rubric. "Zero banned phrases AND ≥1 signal citation AND passes tone classifier" is.

---

## Smoke-Run Results (Delta A)

| System | Pass Rate (held-out, n=50) |
|---|---|
| Week 10 baseline | 72% |
| Trained LoRA (Qwen3-0.6B) | 20% |
| Prompt-only (same backbone) | 26% |

**Delta A: −52 pp** (trained vs. Week 10 baseline, bootstrap CI: −0.68 to −0.34, p < 0.001)

The trained model underperforms the baseline. This is a **smoke-run result** — the held-out
prediction files were generated from stub outputs (unfilled template variables), not live
inference. The negative delta reflects the gap between stub predictions and the scored rubric,
not a regression in the trained model's actual behavior.

Full inference on the held-out set with the deployed adapter is the next step.

---

## Artifacts

| Artifact | Link |
|---|---|
| Dataset (train + dev, 4 configs) | [Nebiyou21/tenacious-bench-v0.1](https://huggingface.co/datasets/Nebiyou21/tenacious-bench-v0.1) |
| LoRA adapter (Qwen3-0.6B) | [Nebiyou21/tenacious-bench-orpo-qwen3-0_6b-lora](https://huggingface.co/Nebiyou21/tenacious-bench-orpo-qwen3-0_6b-lora) |
| Schema | [schema.json](https://github.com/nebiyou27/tenacious-bench/blob/main/schema.json) |

---

## Limitations

- Held-out evaluation used stub predictions; live inference results pending
- Training backbone (Qwen3-0.6B) is small — Qwen3-1.7B may be needed for stable behavior
- Corpus is Tenacious-specific; generalization to other sales contexts is untested
- Dataset size (211 pairs) is thin for robust preference learning

---

*Built as part of TRP1 Week 11 — 10 Academy AI Mastery Program*
