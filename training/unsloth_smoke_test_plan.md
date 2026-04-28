# Unsloth Smoke Test Plan

## Goal

Prove that the Day 5 training path can run on Google Colab T4 before the real preference dataset exists.

## Current Decision

- Runtime: Google Colab T4.
- Model family: Qwen3.5 via Unsloth, starting with the smallest free-Colab notebook option.
- Precision: fp16 on Colab T4; bf16 only for RunPod 4090 or Colab Pro L4 fallback.
- Quantization: do not use QLoRA 4-bit for Qwen3.5 unless the training plan is explicitly revised.
- Dataset: `training/dummy_orpo_preferences.jsonl`.
- Smoke size: five preference records.
- Target artifact: private or disposable HuggingFace adapter repo.

## External References Checked

- Unsloth Qwen3.5 fine-tuning guide: https://unsloth.ai/docs/models/qwen3.5/fine-tune
- General Unsloth fine-tuning guide: https://docs.unsloth.ai/get-started/fine-tuning-llms-guide

## Colab Checklist

1. Start a Colab T4 runtime.
2. Open the smallest available Qwen3.5 Unsloth notebook, preferably Qwen3.5-0.8B or Qwen3.5-2B.
3. Install or update Unsloth in the notebook.
4. Upload or fetch `training/dummy_orpo_preferences.jsonl`.
5. Convert the five records into the notebook's preference format with `prompt`, `chosen`, and `rejected`.
6. Run a minimal LoRA/ORPO training pass.
7. Record compile time, total runtime, package versions, GPU type, and any errors.
8. Push the adapter to a private or disposable HuggingFace repo if the smoke run completes.

## Expected Notes

- First run on T4 may spend several minutes compiling kernels.
- The smoke run is only a compute/path check; it is not a model-quality result.
- If Colab caps or memory errors block the run, use RunPod as the fallback only after recording the exact failure.

## Result Log

| Date | Runtime | Model | Precision | Compile Time | Total Runtime | Adapter Push | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| pending | Colab T4 | Qwen3.5 small notebook | fp16 | pending | pending | scheduled | scheduled | Manual Colab execution required |
