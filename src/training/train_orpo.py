"""Scripted ORPO training entrypoint for the Tenacious Path B critic.

This keeps the training configuration explicit in source control rather than only in notebooks.
It is intentionally LoRA-only and pins the backbone revision for reproducibility.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import sys
from typing import Any

import numpy as np
import torch
from datasets import load_dataset
from peft import LoraConfig, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
from trl import ORPOConfig, ORPOTrainer

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.common import REPO_ROOT


DEFAULT_DATA_PATH = REPO_ROOT / "training_data" / "orpo_preferences.jsonl"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "models" / "orpo_qwen3_0_6b_lora_adapter_scripted"
DEFAULT_BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
DEFAULT_BASE_MODEL_REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"
DEFAULT_LOG_PATH = DEFAULT_OUTPUT_DIR / "training_metrics.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the Path B critic with ORPO and LoRA only.")
    parser.add_argument("--data-path", type=Path, default=DEFAULT_DATA_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-model", default=DEFAULT_BASE_MODEL)
    parser.add_argument("--base-model-revision", default=DEFAULT_BASE_MODEL_REVISION)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--per-device-train-batch-size", type=int, default=4)
    parser.add_argument("--per-device-eval-batch-size", type=int, default=4)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=4)
    parser.add_argument("--num-train-epochs", type=int, default=2)
    parser.add_argument("--warmup-ratio", type=float, default=0.05)
    parser.add_argument("--lr-scheduler-type", default="cosine")
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=32)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    parser.add_argument("--logging-steps", type=int, default=5)
    parser.add_argument("--eval-steps", type=int, default=20)
    parser.add_argument("--save-steps", type=int, default=20)
    parser.add_argument("--max-length", type=int, default=1024)
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--report-to", default="none")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def fix_random_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    set_seed(seed)


def load_preference_dataset(data_path: Path) -> Any:
    dataset = load_dataset("json", data_files=str(data_path))
    train = dataset["train"]
    split = train.train_test_split(test_size=0.1, seed=11)
    return split["train"], split["test"]


def build_model_and_tokenizer(args: argparse.Namespace) -> tuple[Any, Any]:
    tokenizer = AutoTokenizer.from_pretrained(
        args.base_model,
        revision=args.base_model_revision,
        use_fast=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        revision=args.base_model_revision,
        torch_dtype=torch.bfloat16 if args.bf16 else (torch.float16 if args.fp16 else torch.float32),
        device_map="auto",
    )
    return model, tokenizer


def build_lora_config(args: argparse.Namespace) -> LoraConfig:
    return LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )


def build_training_config(args: argparse.Namespace) -> ORPOConfig:
    return ORPOConfig(
        output_dir=str(args.output_dir),
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.per_device_train_batch_size,
        per_device_eval_batch_size=args.per_device_eval_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        num_train_epochs=args.num_train_epochs,
        warmup_ratio=args.warmup_ratio,
        lr_scheduler_type=args.lr_scheduler_type,
        logging_steps=args.logging_steps,
        eval_steps=args.eval_steps,
        save_steps=args.save_steps,
        evaluation_strategy="steps",
        save_strategy="steps",
        logging_strategy="steps",
        report_to=args.report_to,
        max_length=args.max_length,
        bf16=args.bf16,
        fp16=args.fp16,
        seed=args.seed,
    )


def write_training_manifest(args: argparse.Namespace) -> None:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "training_path": "Path B",
        "trainer": "ORPOTrainer",
        "lora_only": True,
        "base_model": args.base_model,
        "base_model_revision": args.base_model_revision,
        "seed": args.seed,
        "learning_rate": args.learning_rate,
        "per_device_train_batch_size": args.per_device_train_batch_size,
        "per_device_eval_batch_size": args.per_device_eval_batch_size,
        "gradient_accumulation_steps": args.gradient_accumulation_steps,
        "num_train_epochs": args.num_train_epochs,
        "warmup_ratio": args.warmup_ratio,
        "lr_scheduler_type": args.lr_scheduler_type,
        "lora_r": args.lora_r,
        "lora_alpha": args.lora_alpha,
        "lora_dropout": args.lora_dropout,
        "max_length": args.max_length,
        "log_path": str(DEFAULT_LOG_PATH),
    }
    (args.output_dir / "training_config.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    fix_random_seed(args.seed)
    write_training_manifest(args)

    train_dataset, eval_dataset = load_preference_dataset(args.data_path)
    if args.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "train_rows": len(train_dataset),
                    "eval_rows": len(eval_dataset),
                    "output_dir": str(args.output_dir),
                },
                indent=2,
            )
        )
        return 0

    model, tokenizer = build_model_and_tokenizer(args)
    lora_config = build_lora_config(args)
    training_config = build_training_config(args)

    trainer = ORPOTrainer(
        model=model,
        args=training_config,
        processing_class=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=lora_config,
    )
    train_result = trainer.train()
    trainer.save_model(str(args.output_dir))
    trainer.save_state()

    DEFAULT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_LOG_PATH.write_text(
        json.dumps(
            {
                "train_runtime": getattr(train_result.metrics, "get", lambda *_: None)("train_runtime")
                if hasattr(train_result, "metrics")
                else None,
                "train_loss": getattr(train_result.metrics, "get", lambda *_: None)("train_loss")
                if hasattr(train_result, "metrics")
                else None,
                "eval_rows": len(eval_dataset),
                "train_rows": len(train_dataset),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "completed",
                "output_dir": str(args.output_dir),
                "train_rows": len(train_dataset),
                "eval_rows": len(eval_dataset),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
