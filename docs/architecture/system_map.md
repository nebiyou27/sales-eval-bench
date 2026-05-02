# System Map

## End-to-End Flow

1. `seed/`
Week 10 probes, trace logs, held-out trace IDs, and failure taxonomy provide the benchmark's
evidence base.

2. `src/generation/`
Authoring scripts materialize four task sources:
- trace-derived
- programmatic
- synthetic
- hand-authored adversarial

3. `tenacious_bench_v0.1/`
Generated tasks are partitioned into `train/`, `dev/`, and sealed `held_out/`.

4. `src/generation/contamination_check.py`
Held-out integrity is checked against train/dev using n-gram overlap, lexical similarity, embedding
similarity, time-shift provenance, and source-trace leakage.

5. `src/generation/judge_filter.py`
Synthetic-task admission is gated with pointwise scoring, duplicate checks, and calibration sampling.

6. `src/training/build_orpo_preferences.py` and `src/training/prepare_orpo_data.py`
Public benchmark rows are transformed into preference pairs while enforcing provenance and model-family
rotation policy.

7. `src/training/train_orpo.py`
The Path B critic is trained with ORPO and LoRA-only adaptation.

8. `src/scoring/`
Candidate outputs, rubric checks, and inter-rater scaffolding are scored and summarized here.

9. `src/ablations/run_ablation.py`
Delta A, Delta B, Delta C, and Cost-Pareto comparisons are run from one shared harness.

## Boundary Rules

- `seed/` is evidence, not training data.
- `held_out/` is evaluation-only and must never enter training prep.
- `docs/` is for narrative truth; `reports/` is for generated outputs.
- `notebooks/` may explore, but `src/` owns production logic.
