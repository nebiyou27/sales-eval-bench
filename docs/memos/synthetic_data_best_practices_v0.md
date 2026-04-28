# Common Reading Memo v0: Synthetic Data Best Practices

Paper: Ruibo Liu et al., "Best Practices and Lessons Learned on Synthetic Data",
arXiv:2404.07503v2, COLM 2024.

## Claim I Will Use

Synthetic data is useful for Tenacious-Bench only when it is generated under controlled
domain constraints and then filtered for factuality, fidelity, bias, and leakage risk. The
paper's strongest practical warning is that synthetic data can improve coverage and lower
cost, but noisy or ungrounded synthetic examples can also teach the exact behavior the
benchmark is supposed to catch.

For Week 11, this means the dataset should not be "more sales examples." It should be a
targeted set of hard, Tenacious-specific failure cases: gap-condescension, AI-maturity
inconsistency, signal overclaiming, invalid output shape, and weak buyer-next-step quality.

## Design Choice It Changes

Days 2-3 dataset authoring should use a three-stage gate:

1. Generate from hand-authored probes and trace-derived templates, not open-ended prompts.
2. Require provenance fields for every signal-grounded task: source mode, source type,
   retrieval date if applicable, and the specific buyer signal that the output may use.
3. Filter examples before training or evaluation with deterministic checks first, then a
   different model-family judge for semantic checks.

The concrete repo decision is that `src/generation/generate_synthesis.py` should emit
generation metadata alongside each candidate, and `src/generation/contamination_check.py`
should run before any generated example can enter `held_out/`. The existing
`schema.json` fields for `source_mode`, `failure_dimension`, `scoring_config`, and
`metadata` are therefore not optional bookkeeping; they are quality-control surfaces.

## Where I Disagree

The paper is broad and treats synthetic-data quality mostly as a general property:
factuality, fidelity, unbiasedness, diversity, and contamination. For Tenacious-Bench, the
harder failure is narrower: a candidate can be factually grounded and still be commercially
bad because it assumes a buyer is unsophisticated, overstates an AI gap, or turns a weak
signal into an intrusive claim.

So I will not accept generic "high quality" LLM judgments as sufficient. The rubric needs
dimension-specific checks for buyer respect, signal entitlement, and Tenacious style. This
is why Path B remains a judge/critic rather than just an SFT dataset expansion.

## Evidence I Will Collect

- Rejection rate by failure dimension during synthesis filtering.
- Near-duplicate rate from n-gram and embedding contamination checks.
- Human spot-check notes for at least 30 calibration tasks before held-out sealing.
- Disagreement cases where deterministic checks pass but the judge rejects the output.
- Cost per accepted synthetic task, logged in `cost/log.csv`.

## Repo Artifact Affected

- `schema.json`: keep provenance, partition, failure dimension, and scoring config required.
- `src/generation/generate_synthesis.py`: generate from controlled probe templates with
  metadata, not free-form bulk prompts.
- `src/generation/contamination_check.py`: enforce held-out separation before sealing.
- `docs/methodology.md`: cite this memo as the Day 0 reason for metadata-heavy schema design and
  model-family rotation.
- `docs/cost_controls.md`: preserve the no eval-tier authoring/dedup rule for Days 2-3 because
  low-cost generation is acceptable only if filtering is strict.

## Source Notes

The paper argues that synthetic data can address scarcity, privacy, and annotation cost, but
also stresses factuality, fidelity, bias control, responsible use, and contamination risk.
It specifically notes that synthetic data can help evaluation and scalable oversight, while
also making benchmark decontamination harder because rephrased benchmark data can evade
token-level checks. For Tenacious-Bench, the actionable lesson is to prefer fewer,
well-instrumented synthetic tasks over high-volume untracked generation.
