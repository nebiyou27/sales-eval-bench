# Common Reading Memo v1: Judge Rotation and Preference Leakage

Reading focus: model-family rotation for synthetic generation and preference filtering.

## Claim I Will Use

If the same model family both generates and judges the same synthetic example, the acceptance rate
can become artificially optimistic. For Tenacious-Bench, that matters because the benchmark is
trying to catch subtle failures such as condescension, unsupported signaling, and overconfident
next steps, not just obvious formatting errors.

The practical rule I am taking forward is simple: do not let one family grade its own homework.
Generation and judging should be separated by model family, and preference-pair prep should enforce
the same separation for chosen rewrites and rejected outputs.

## Design Choice It Changes

This reading locks in four repo decisions:

1. `src/generation/generate_synthesis.py` must require a distinct judge family for live synthesis.
2. Synthetic rows must record the generation model, judge model, prompt version, and seed so later
   auditing can confirm how a row entered the corpus.
3. Preference prep must reject any pair where the chosen-rewrite judge shares a family with either
   the chosen-rewrite generator or the rejected-output author.
4. Duplicate filtering belongs in generation, not only in downstream contamination reports, because
   repeated accepted outputs can hide low diversity behind apparently successful judge passes.

## Where I Disagree

General "LLM-as-a-judge" optimism is too broad for this project. A strong model can still approve
its own stylistic habits, especially in short sales messages where the surface form is fluent but
the commercial behavior is wrong. For Tenacious-Bench, a polished message that still talks down to
the buyer or overstates a weak signal is a failure.

So I am not treating same-family generation plus judging as acceptable just because the task looks
easy. The safer default is separation plus metadata, even on a small budget.

## Evidence I Will Collect

- Acceptance rate by generation family and judge family.
- Count of synthetic rows skipped for duplicate output.
- Count of preference rows rejected for rotation-policy violations.
- Cases where deterministic checks pass but the rotated judge still returns `revise` or `block`.
- Cost per accepted synthetic task after duplicate filtering and judge rejection.

## Repo Artifacts Affected

- `src/generation/generate_synthesis.py`: keep rotation mandatory, stamp seeds, and skip duplicate
  candidate outputs before writing accepted rows.
- `src/training/prepare_orpo_data.py`: continue to reject preference pairs that violate family
  rotation.
- `docs/methodology.md`: cite this memo when explaining the multi-LLM routing policy and why
  duplicate filtering is part of generation quality control rather than just held-out hygiene.
- `docs/datasheet.md`: describe synthetic generation as metadata-rich and rotation-controlled, not
  as open-ended sampling.

## Source Notes

The project methodology already treats preference leakage as a real risk. This memo turns that from
a general warning into an implementation rule: separate model families, log the lineage, and keep
generation reproducible enough to audit later. For a small benchmark, that discipline matters more
than squeezing out a few extra synthetic rows.
