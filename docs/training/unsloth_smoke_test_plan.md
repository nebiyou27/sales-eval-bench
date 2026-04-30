# Unsloth Smoke Test Plan

## Goal

Verify the Day 5 training path can run end-to-end on Google Colab T4 before the real
preference dataset exists. This is a compute/path check only — not a model-quality result.

---

## Fixed Parameters (do not change for smoke run)

| Parameter | Value | Reason |
|---|---|---|
| Model | `unsloth/Qwen3-0.6B` | Smallest Qwen3; fits T4 16 GB comfortably |
| Precision | `fp16=True` | T4 does not support bf16; bf16 only for L4/4090 |
| Quantization | None (full fp16) | No QLoRA 4-bit until smoke confirms stability |
| Algorithm | ORPO | Reference-free, single-stage, no separate reward model |
| Dataset | `tenacious_bench_v0.1/smoke/dummy_orpo_preferences.jsonl` | 5 records, all source IDs verified |
| Adapter target | Private or disposable HuggingFace repo | Discard after smoke; not the production adapter |

---

## LoRA Config

```python
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-0.6B",
    max_seq_length=512,       # smoke only; production will use 1024+
    dtype=None,               # Unsloth auto-selects fp16 on T4
    load_in_4bit=False,       # no QLoRA for smoke
)

model = FastLanguageModel.get_peft_model(
    model,
    r=8,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0.0,         # 0 is standard for ORPO
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
)
```

---

## ORPO Training Config

```python
from trl import ORPOConfig, ORPOTrainer

orpo_args = ORPOConfig(
    learning_rate=2e-5,
    beta=0.1,                         # ORPO margin penalty weight
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1,
    max_steps=5,                      # smoke: one step per record
    warmup_steps=0,
    fp16=True,
    bf16=False,
    logging_steps=1,
    output_dir="orpo_smoke_adapter",
    optim="adamw_8bit",               # Unsloth default
    max_length=512,
    max_prompt_length=256,
    remove_unused_columns=False,
)
```

---

## Pre-Flight Checklist (run locally before opening Colab)

- [ ] **1. Dry-run prepare_orpo_data.py**

  ```
  .\.venv\Scripts\python.exe src/training/prepare_orpo_data.py \
    --input tenacious_bench_v0.1/smoke/dummy_orpo_preferences.jsonl \
    --output C:\tmp\dummy_orpo_prepared.jsonl \
    --dry-run
  ```

  **Expected output** (printed JSON):
  ```json
  {
    "input_count": 5,
    "prepared_count": 5,
    "dropped_count": 0,
    "output_partition": "train"
  }
  ```
  Stop and fix any `dropped_count > 0` before proceeding.

- [ ] **2. Confirm source task IDs resolve** — already verified: all 5 smoke records map to
  real task IDs in `train/` and `dev/` partitions. No held_out references.

- [ ] **3. Confirm no held_out contamination** — smoke records cite only
  `source_partition: train` or `source_partition: dev`. ✓

---

## Colab Run Checklist

- [ ] **Step 1 — Start runtime**
  - Runtime → Change runtime type → T4 GPU
  - Confirm: `!nvidia-smi` shows Tesla T4, ~15 GB free VRAM

- [ ] **Step 2 — Install Unsloth**
  ```python
  !pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
  !pip install trl>=1.0.0 transformers>=4.40.0 accelerate peft datasets
  ```
  Record the installed versions of `unsloth`, `trl`, `transformers`, `torch`.

- [ ] **Step 3 — Upload smoke dataset**
  Upload `tenacious_bench_v0.1/smoke/dummy_orpo_preferences.jsonl` via the Colab Files
  panel, or copy-paste the 5 records inline as a Python list of dicts.

- [ ] **Step 4 — Format data for ORPO**
  ORPO trainer expects `{"prompt": ..., "chosen": ..., "rejected": ...}`. The smoke records
  already have these fields. Load with:
  ```python
  import json
  from datasets import Dataset

  records = [json.loads(l) for l in open("dummy_orpo_preferences.jsonl")]
  ds = Dataset.from_list([{"prompt": r["prompt"],
                            "chosen": r["chosen"],
                            "rejected": r["rejected"]} for r in records])
  ```

- [ ] **Step 5 — Load model and apply LoRA** — use the LoRA config above verbatim.

- [ ] **Step 6 — Run ORPO training** — use the ORPO config above verbatim.
  ```python
  trainer = ORPOTrainer(model=model, args=orpo_args, train_dataset=ds, tokenizer=tokenizer)
  trainer.train()
  ```

- [ ] **Step 7 — Save adapter**
  ```python
  model.save_pretrained("orpo_smoke_adapter")
  tokenizer.save_pretrained("orpo_smoke_adapter")
  ```

- [ ] **Step 8 — (Optional) Push to HuggingFace**
  Push to a private or throwaway repo only. Do not push to the production adapter repo.

- [ ] **Step 9 — Record run metrics** in the Result Log table below.

---

## Expected Outputs

| Output | Description |
|---|---|
| `orpo_smoke_adapter/adapter_config.json` | LoRA config, confirms r=8 and target modules |
| `orpo_smoke_adapter/adapter_model.safetensors` | Adapter weights, should be ~10–30 MB |
| Training log (5 rows) | One loss entry per step; all finite |
| `nvidia-smi` VRAM peak | Should stay under 14 GB with batch_size=1 |

---

## Pass / Fail Criteria

### PASS — all of the following:
- All 5 training steps complete without exception
- Every logged loss value is finite (not `nan`, not `inf`)
- `adapter_config.json` exists and contains `"r": 8`
- Peak VRAM stays below 14 GB
- Total runtime under 15 minutes

### FAIL — any of the following, with required action:

| Failure | Required action before Day 5 |
|---|---|
| CUDA OOM | Try `gradient_accumulation_steps=2`, `max_length=256`. If still OOM, note exact error and evaluate Qwen3-1.7B skip. |
| `nan` or `inf` loss at step 1 | Check data format; tokenizer BOS/EOS; `beta` value. |
| Unsloth import error | Pin `unsloth` commit hash; record in Result Log. |
| Runtime disconnects before step 5 | Re-run; note whether it is a Colab timeout or OOM crash. |
| `adapter_model.safetensors` missing | Training completed but save failed — check disk quota. |

---

## Result Log

| Date | Runtime | Model | Precision | LoRA r | Compile Time | Total Runtime | Peak VRAM | Adapter Saved | Result | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| pending | Colab T4 | Qwen3-0.6B | fp16 | 8 | pending | pending | pending | no | scheduled | — |
