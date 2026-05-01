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
