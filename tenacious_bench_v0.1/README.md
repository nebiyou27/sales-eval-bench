# Tenacious-Bench v0.1 (Data Surfaces)

Benchmark task rows. Code lives in `src/`; this directory is data only.

| Path | Status | Use |
|---|---|---|
| `train/` | versioned | LoRA training surface (132 tasks). |
| `dev/` | versioned | Iteration and rubric calibration (79 tasks). |
| `held_out/` | local, gitignored | Sealed evaluation only (50 tasks). Never enters training prep. |
| `smoke/` | versioned | Tiny dummy fixtures used by unit tests and CI smoke. |

## Authoring rules

- Schema is `schema.json` at the repo root; every row must validate.
- Source mode is recorded in `metadata.source_mode`: `trace_derived`, `programmatic`,
  `synthetic`, or `hand_authored`.
- Trace-derived rows must not cite a `source_trace_id` listed in `seed/held_out_traces.jsonl`.
- Synthetic rows must record `prompt_version`, generation model, judge model, and seed in
  `metadata`; rotation policy (`src/generation/synthesis_policy.py`) blocks same-family
  generate-and-judge pairs.

## Adding rows

Generate via the four authoring entrypoints under `src/generation/`, then run
`src/generation/contamination_check.py` before sealing any change to `held_out/`. Manifest files
ending in `_prompt_manifest.jsonl` are generation artifacts, not benchmark rows.
