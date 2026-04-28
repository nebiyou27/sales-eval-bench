# PRD — Sales Eval Bench (TRP1 Week 11)

## What we are building

A Tenacious-specific evaluation benchmark (Tenacious-Bench v0.1) and a trained LoRA judge
(Path B — ORPO) that lifts the Week 10 Conversion Engine on its two measured failure modes.

## Acceptance Criteria

### Dataset (Acts I–II)
- [ ] 200–300 machine-verifiable tasks across Tenacious-specific failure dimensions
- [ ] 4 authoring modes represented: trace-derived, programmatic, synthesis, hand-authored
- [ ] 3 partitions: train 50% / dev 30% / held_out 20%
- [ ] Contamination checks passed: n-gram (<8-gram overlap), embedding (<0.85 cosine), time-shift
- [ ] Inter-rater agreement ≥80% on every rubric dimension
- [ ] Datasheet covering all 7 Gebru sections + Pushkarna layered detail
- [ ] Published to HuggingFace with CC-BY-4.0 license

### Training (Acts III–IV)
- [ ] LoRA adapter trained with ORPO on Qwen3-0.6B, or Qwen3-1.7B if the T4 smoke run is stable, via Unsloth on Colab T4
- [ ] Training loss curve logged
- [ ] Delta A positive on held-out with 95% CI, p < 0.05 (paired bootstrap)
- [ ] Delta B reported honestly (trained vs prompt-only same backbone)
- [ ] Cost-Pareto reported (cost + latency with vs without trained component)
- [ ] Model card complete and published to HuggingFace

### Public artifacts (Act V)
- [ ] HuggingFace dataset URL live (no login required)
- [ ] HuggingFace model URL live (no login required)
- [ ] Blog post published (1,200–2,000 words, HuggingFace community / Substack)
- [ ] Community engagement: GitHub issue on τ²-Bench repo linking Tenacious-Bench
- [ ] 2-page memo (Page 1: decision + lift + recommendation; Page 2: skeptic's appendix)
- [ ] Demo video (max 6 min): dataset on HuggingFace, one task scored end-to-end, ablation trace

### Cost
- Total spend: ≤ $10
- Every charge logged in cost_log.csv

## Minimum Uplift
- Delta A > 0 on Tenacious-Bench held-out (any positive lift with statistical significance)
- Zero preference leakage (no same-family generate+judge pairs)
- Held-out sealed and never touched by training scripts

## Deadlines
- Wed Apr 30, 21:00 UTC — Acts I + II (GitHub repo + PDF interim report)
- Sat May 3, 21:00 UTC — Acts III–V (all public artifacts + final submission)
