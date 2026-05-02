# Notebooks (Exploration Only)

| Notebook | Purpose |
|---|---|
| `unsloth_orpo_smoke_test.ipynb` | Day 5 smoke pass on Colab T4 to validate the Unsloth+TRL ORPO loop end-to-end on a tiny preference subset. |
| `unsloth_orpo_full_train.ipynb` | Full ORPO LoRA run on the prepared preference corpus; saves the adapter to `models/orpo_qwen3_0_6b_lora_adapter/`. |

Notebooks are scratch / runbook surfaces. Anything productionized belongs under `src/`.
Hyperparameters and run config should be promoted into `configs/` as they stabilize.
