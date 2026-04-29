"""Download the local sentence-embedding model used by contamination checks."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from huggingface_hub import snapshot_download

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.generation.contamination_check import DEFAULT_EMBEDDING_MODEL, DEFAULT_LOCAL_EMBEDDING_DIR

DEFAULT_ALLOW_PATTERNS = [
    "config.json",
    "config_sentence_transformers.json",
    "modules.json",
    "sentence_bert_config.json",
    "pytorch_model.bin",
    "model.safetensors",
    "tokenizer.json",
    "tokenizer_config.json",
    "special_tokens_map.json",
    "vocab.txt",
    "vocab.json",
    "merges.txt",
    "1_Pooling/config.json",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch the local embedding model required for semantic contamination checks."
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_EMBEDDING_MODEL,
        help="Hugging Face model id to download.",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=DEFAULT_LOCAL_EMBEDDING_DIR,
        help="Local directory where the model snapshot should be stored.",
    )
    parser.add_argument(
        "--revision",
        default=None,
        help="Optional model revision to pin.",
    )
    parser.add_argument(
        "--include-all-files",
        action="store_true",
        help="Download the full repo snapshot instead of only the files needed for local embeddings.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_dir = args.target_dir
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=args.model,
        revision=args.revision,
        local_dir=str(target_dir),
        allow_patterns=None if args.include_all_files else DEFAULT_ALLOW_PATTERNS,
    )
    print(f"Downloaded {args.model} to {target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
