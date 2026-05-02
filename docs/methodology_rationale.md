# Methodology Rationale

## Path Choice

This project uses **Path B: a preference-tuned judge / critic** trained with **ORPO**. The Week 10 evidence points more strongly to inconsistency failures than to purely generative failures. The system often produces something plausibly useful, but it does not reliably detect when its own output is unsupported, overconfident, invalid, or condescending. That makes a critic layer a better intervention than a pure generation rewrite.

The two anchor failure modes are:

- **P24 - AI-maturity inconsistency**: hard tasks sometimes return invalid or empty JSON while the system still treats the result as acceptable.
- **P33 - Gap-condescension**: the agent can generate language that is overly presumptuous toward technically sophisticated buyers and lacks a reliable internal check to stop it.

These are both cases where the core need is better detection and ranking of outputs, not only more fluent output generation. That is why Path B is the primary training path.

## Why ORPO

ORPO is the best fit for this repo because it is **reference-free**, uses a **single-stage objective**, and stays practical inside the Week 11 Colab T4 budget. The prepared training rows already have the shape ORPO wants: each record contains a shared prompt, a preferred `chosen` output, and a worse `rejected` output. That lets the training run stay simple and auditable.

Compared with the alternatives:

- **DPO** is a strong baseline, but it requires a reference policy during training and adds more moving parts than this budget really needs.
- **SimPO** is also reference-free, but ORPO is a cleaner fit for short sales-response preferences and the repo was already scaffolded around ORPO-style data preparation.

## Evidence And Data Policy

The ORPO corpus in `training_data/orpo_preferences.jsonl` is built only from public `train` and `dev` benchmark rows. The held-out split remains sealed and excluded from training prep. This matches the contamination policy documented in the benchmark methodology and keeps the training run aligned with the Week 11 challenge requirement that held-out evaluation stay separate from training.

The preference rows also preserve provenance fields such as `source_task_id`, `source_partition`, `chosen_source`, `rejected_source`, and `rejected_model`, which supports later auditing and preference-leakage checks.

## Week 10 Trace Evidence

Path B is anchored in five concrete reward-0.0 trace IDs from the Week 10 Conversion Engine run.
These traces are cited as justification only; they are excluded from `train` and `dev` partitions
under the held-out leakage check in `src/generation/contamination_check.py`.

- `a553180f-80d2-4d4b-9a1e-d525b1219cfd` (task 11) — competitor-gap condescension (P33). The agent
  produced a gap-language reply on weak peer-hiring signal, which is the exact failure mode the
  trained critic must learn to reject.
- `89337dd1-bb36-41d7-8530-190df8734cc3` (task 34) — AI-maturity inconsistency (P24). The agent
  returned an empty/invalid maturity payload while the surrounding scoring still treated the run as
  acceptable; the critic must learn to mark this `revise` rather than `accept`.
- `ef2ad255-479a-4b67-a96f-2522026e3aaf` (task 66) — unsupported-evidence overclaim. The agent
  asserted a workflow gap from a thin public signal; the critic must enforce abstention.
- `0857ba6e-d8cb-4ec8-b024-3d5ddc298fc6` (task 76) — fixture/live boundary honesty (P30). The
  agent treated a fixture-backed artifact as production evidence; the critic must demote any
  output that crosses that boundary.
- `19d13ac9-f495-4df4-b1c4-d042ca754933` (task 92) — thin-evidence restraint (P29). The agent
  failed to abstain when the public-signal window was too small to support the claim.

Together these five trace IDs map directly to the inconsistency-class failures that motivate
Path B over Path A (generation rewrite) or Path C (PRM/trajectory). Each trace gives the rejected
side of at least one ORPO preference pair after relabeling under the rotation policy; the chosen
side is materialized at preference-prep time, never inlined into a benchmark row.

## Paper Anchors

The rationale is grounded in at least two of the required readings:

- **Hong, Lee, and Thorne (2024), ORPO: Monolithic Preference Optimization without Reference Model**: supports the choice of a reference-free preference objective that combines supervised learning with odds-ratio preference optimization in one stage.
- **Rafailov et al. (2023), Direct Preference Optimization**: provides the baseline contrast case and clarifies why avoiding a reference model is useful here.
- **Liu et al. (2024), Best Practices and Lessons Learned on Synthetic Data for Language Models**: supports the use of controlled, provenance-rich synthetic or rewritten examples instead of uncontrolled volume generation.
- **Gu et al. (2024-2025), A Survey on LLM-as-a-Judge**: supports the broader design direction that evaluator quality and calibration matter as much as raw generator quality in domain-specific benchmark settings.

## Act III Decision

The practical Act III decision is:

- train a small LoRA critic with ORPO,
- start with the prepared public-only preference corpus,
- run the first full Colab training pass on a small Qwen backbone,
- save the adapter and training artifacts,
- then move into Act IV ablations against the sealed held-out split.
