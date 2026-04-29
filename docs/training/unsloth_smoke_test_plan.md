# Unsloth Smoke Test Plan

## Goal

Prove that the Day 5 training path can run on Google Colab T4 before the real preference dataset exists.

## Current Decision

- Runtime: Google Colab T4.
- Model target: Qwen3-0.6B via Unsloth for the first smoke run; Qwen3-1.7B is the fallback only if T4 memory and runtime are stable.
- Precision: fp16 on Colab T4; bf16 only for RunPod 4090 or Colab Pro L4 fallback.
- Quantization: do not use QLoRA 4-bit unless the training plan is explicitly revised after the smoke run.
- Dataset: `tenacious_bench_v0.1/smoke/dummy_orpo_preferences.jsonl`.
- Smoke size: five preference records.
- Target artifact: private or disposable HuggingFace adapter repo.

## External References Checked

- Unsloth Qwen3 fine-tuning guide: https://unsloth.ai/docs/models/qwen3-how-to-run-and-fine-tune
- General Unsloth fine-tuning guide: https://docs.unsloth.ai/get-started/fine-tuning-llms-guide

## Colab Checklist

1. Start a Colab T4 runtime.
2. Open the smallest available Qwen3 Unsloth notebook and set the model to Qwen3-0.6B for the first run.
3. Install or update Unsloth in the notebook.
4. Upload or fetch `tenacious_bench_v0.1/smoke/dummy_orpo_preferences.jsonl`.
5. Run `.\.venv\Scripts\python.exe src/training/prepare_orpo_data.py --input tenacious_bench_v0.1/smoke/dummy_orpo_preferences.jsonl --output C:\tmp\dummy_orpo_prepared.jsonl --dry-run` locally first and confirm `prepared_count=5`, `dropped_count=0`, and `output_partition=train`.
6. Convert the five records into the notebook's preference format with `prompt`, `chosen`, and `rejected`.
7. Run a minimal LoRA/ORPO training pass.
8. Record compile time, total runtime, package versions, GPU type, and any errors.
9. Push the adapter to a private or disposable HuggingFace repo if the smoke run completes.

## Expected Notes

- First run on T4 may spend several minutes compiling kernels.
- The smoke run is only a compute/path check; it is not a model-quality result.
- If Colab caps or memory errors block the run, use RunPod as the fallback only after recording the exact failure.

## Result Log

| Date | Runtime | Model | Precision | Compile Time | Total Runtime | Adapter Push | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| pending | Colab T4 | Qwen3-0.6B | fp16 | pending | pending | scheduled | scheduled | Manual Colab execution required |
