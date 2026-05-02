# Configs

This directory is reserved for stabilized configuration files that should not stay embedded in
CLI flags forever.

Recommended future layout:

- `configs/training/`: LoRA and ORPO hyperparameter presets
- `configs/evaluation/`: ablation and held-out run presets
- `configs/generation/`: synthesis and judge-filter presets

The current repo still keeps most configuration in source for auditability, but this is the
intended landing zone as the project matures.
