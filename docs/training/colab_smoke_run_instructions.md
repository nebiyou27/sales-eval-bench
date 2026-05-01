# Colab Smoke Run Instructions

Use [unsloth_orpo_smoke_test.ipynb](/d:/TRP-1/week-11/Sales%20Eval%20Bench/notebooks/unsloth_orpo_smoke_test.ipynb) for the Colab ORPO smoke run. This notebook is intentionally limited to the 5-record smoke dataset at `tenacious_bench_v0.1/smoke/dummy_orpo_preferences.jsonl` and must not be repointed at `training_data/orpo_preferences.jsonl`.

## Open in Colab

1. Upload or sync the repo so Colab can access it.
2. Open Colab and choose `File -> Upload notebook`, then select `notebooks/unsloth_orpo_smoke_test.ipynb`.
3. In the repo-access cell, choose one mode:
   - `drive`: if the repo already exists in Google Drive.
   - `clone`: if you want Colab to clone the repo directly.

## Runtime

Select `Runtime -> Change runtime type` and use:

- Runtime type: `Python 3`
- Hardware accelerator: `T4 GPU`

The notebook includes a GPU / VRAM check cell. Stop there if CUDA is unavailable.

## What to run

Execute the notebook top to bottom. The cells that require manual Colab execution are:

1. Install dependencies.
2. Check GPU / VRAM.
3. Mount Drive or clone the repo.
4. Load and validate the 5-record smoke dataset.
5. Load `unsloth/Qwen3-0.6B`.
6. Apply LoRA.
7. Run exactly 5 ORPO smoke steps.
8. Save and verify the adapter.
9. Write `smoke_result.json`.

Do not skip the dataset validation cell. It enforces the expected smoke-record count of 5.

## Files to copy back after the run

Copy the full smoke output folder back into the repo if the run happened in a temporary Colab workspace:

- `smoke_outputs/orpo_unsloth_qwen3_0_6b_fp16_smoke/adapter_config.json`
- `smoke_outputs/orpo_unsloth_qwen3_0_6b_fp16_smoke/adapter_model.safetensors`
- `smoke_outputs/orpo_unsloth_qwen3_0_6b_fp16_smoke/smoke_result.json`
- Any tokenizer files saved in that same folder

If you used the `drive` path and pointed Colab at the repo already stored in Drive, those artifacts should already be inside the repo tree.

## Where to record the result

After the run, add a new top entry to [docs/progress.md](/d:/TRP-1/week-11/Sales%20Eval%20Bench/docs/progress.md) with:

- Run date
- Runtime used, such as `Colab T4`
- Result: `pass` or `fail`
- Peak VRAM if available
- Whether `adapter_config.json` and `adapter_model.safetensors` were saved
- Any failure mode notes such as OOM, NaN loss, import error, or missing adapter artifact

Reference `docs/training/unsloth_smoke_test_plan.md` if you want the broader acceptance criteria alongside the notebook.
