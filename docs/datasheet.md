# Tenacious-Bench v0.1 Datasheet

This datasheet follows the seven-section structure from Gebru et al. and uses a Pushkarna-style
layering pattern:

- Telescopic: what the corpus is for.
- Periscopic: how the corpus is organized and produced.
- Microscopic: the concrete fields, checks, and known gaps.

## 1. Motivation

**Telescopic summary.** Tenacious-Bench v0.1 is a machine-verifiable benchmark for evaluating
Tenacious sales-agent outputs on the failure modes that mattered most in Week 10: gap
condescension, AI-maturity inconsistency, signal overclaiming, output validity, style-guide
drift, and weak buyer next steps.

**Periscopic structure.** The benchmark is intended for three linked uses:

- scoring candidate outputs with deterministic checks first and judge-backed checks second,
- preparing ORPO preference data for a small judge or critic model,
- running sealed held-out comparisons against prompt-only and trained-critic baselines.

**Who created it and why.** Nebiyou Abebe created the dataset for 10 Academy TRP1 Week 11 so the
project can move from "the model often sounds fine" to "the system can reliably accept, revise, or
block risky outreach before it is sent."

**Funding and cost posture.** No external funding. The repo assumes low-cost authoring and keeps
generation, filtering, and contamination work in the dev-tier budget, with all live calls logged
to `cost/log.csv`.

## 2. Composition

**Telescopic summary.** The current validated corpus in this workspace contains 261 tasks: 132
`train`, 79 `dev`, and 50 local sealed `held_out`. The public training surface is 211 tasks
(`train` + `dev`), while `held_out` remains excluded from training use.

The held-out split now reaches the 50-task target and passes the contamination gate, but human
agreement work is still pending, so the corpus should not yet be described as fully
human-calibrated.
The committed repo includes the generator code, tests, documentation, and contamination report for
that sealed split, but the 50 held-out task rows themselves remain local and gitignored.

### Partition counts

| partition | count | note |
|---|---:|---|
| `train` | 132 | committed |
| `dev` | 79 | committed |
| `held_out` | 50 | local, gitignored, sealed for evaluation |
| **total** | **261** | |

### Failure-dimension coverage

For the public authoring surface (`train` + `dev`):

| failure_dimension | train | dev | total |
|---|---:|---:|---:|
| `gap_condescension` | 25 | 14 | 39 |
| `ai_maturity_consistency` | 25 | 14 | 39 |
| `output_validity` | 22 | 14 | 36 |
| `signal_grounding` | 21 | 11 | 32 |
| `style_guide_adherence` | 22 | 17 | 39 |
| `next_step_quality` | 17 | 9 | 26 |
| **total** | **132** | **79** | **211** |

For the sealed `held_out` split:

| failure_dimension | held_out |
|---|---:|
| `gap_condescension` | 12 |
| `ai_maturity_consistency` | 12 |
| `signal_grounding` | 12 |
| `style_guide_adherence` | 2 |
| `next_step_quality` | 10 |
| `output_validity` | 2 |

### Source-mode coverage

| source_mode | train | dev | held_out | total |
|---|---:|---:|---:|---:|
| `programmatic` | 72 | 51 | 0 | 123 |
| `trace_derived` | 36 | 24 | 0 | 60 |
| `hand_authored` | 17 | 0 | 50 | 67 |
| `synthetic` | 7 | 4 | 0 | 11 |
| **total** | **132** | **79** | **50** | **261** |

### Difficulty, channel, and message-kind coverage

Full validated corpus in this workspace:

| field | values |
|---|---|
| `difficulty` | `hard` 132, `medium` 71, `easy` 58 |
| `channel` | `email` 182, `linkedin_dm` 70, `sms` 9 |
| `message_kind` | `warm_reply` 110, `cold_outreach` 92, `reengagement` 59 |

**Microscopic schema detail.** Every task is a JSON object validated against `schema.json` and
includes the following required top-level fields:

- `task_id`
- `partition`
- `source_mode`
- `difficulty`
- `failure_dimension`
- `channel`
- `message_kind`
- `input`
- `candidate_output`
- `ground_truth`
- `rubric`
- `scoring_config`
- `metadata`

The `input` object carries prospect context, signal summaries, benchmark constraints, and prior
thread context. `candidate_output` carries the message body and, for email, a subject line.
`rubric` holds expected terms, banned phrases, and formatting constraints. `scoring_config`
declares which dimensions are deterministic and which require judge-backed review.

## 3. Collection Process

**Telescopic summary.** The corpus is assembled through four authoring modes so the benchmark can
cover grounded reconstruction, deterministic variation, deliberately hard adversarial cases, and
limited live synthesis.

### Trace-derived tasks

`src/generation/generate_trace_derived.py` turns Week 10 failure-trace metadata from
`seed/trace_log.jsonl` into task templates without copying the original full prompt/output payloads
into the repo. Any cited trace ID is checked against `seed/held_out_traces.jsonl` before a task is
allowed into `train` or `dev`.

### Programmatic tasks

`src/generation/generate_programmatic.py` expands deterministic blueprints across prospect and
message variants. This path does not call an LLM and is used for broad, auditable coverage of known
failure patterns.

### Hand-authored tasks

`src/generation/generate_hand_authored.py` encodes explicitly difficult Week 10 probe-derived cases,
including condescension risk, unsupported evidence, duplicate-send recovery, timeline gating, and
fixture-versus-production honesty.

### Synthetic tasks

`src/generation/generate_synthesis.py` supports:

- offline prompt-manifest generation,
- live generation with a distinct judge model,
- explicit seed stamping in manifests and accepted rows,
- duplicate filtering against existing synthetic outputs and the current batch,
- metadata capture for prompt version, generation model, judge model, and seed.

The current committed synthetic count is 11 accepted tasks: 7 in `train` and 4 in `dev`.

**Data freshness and fictionalization.** The benchmark is grounded in April 2026 Week 10 artifacts,
but the committed tasks use fictional company and contact contexts. The repo does not publish real
prospect identities.

## 4. Preprocessing, Cleaning, and Labeling

**Telescopic summary.** A task is not admitted to the benchmark just because it exists. It must
clear schema validation, held-out leakage checks, and contamination checks before it counts as
usable data.

### Validation and cleaning steps

1. `validate_task(...)` in `src/generation/common.py` validates each row against `schema.json`.
2. `assert_no_held_out_leakage(...)` blocks any `train` or `dev` task that cites a trace ID found
   in `seed/held_out_traces.jsonl`.
3. `src/generation/contamination_check.py` audits overlap between `held_out` and `train` or `dev`
   using 8-gram overlap, lexical cosine, and MiniLM embedding cosine when the local embedding model
   is available.
4. `src/generation/generate_synthesis.py` now filters exact near-duplicates at generation time by
   normalizing `candidate_output.subject` and `candidate_output.body` together with channel,
   message kind, and failure dimension.

### Labeling policy

`ground_truth.target_decision` records whether the candidate should be `accept`, `revise`, or
`block`. The currently committed benchmark rows are positive benchmark tasks whose candidate outputs
represent the intended behavior for their scenario. Rejected alternatives for ORPO are materialized
separately during preference-data preparation, not stored inline as extra rows in the benchmark
itself.

### Deterministic versus judge-backed scoring

The benchmark is machine-verifiable first. Deterministic checks cover shape, length, forbidden
terms, banned phrases, and single-ask discipline. Judge-backed dimensions are used only where the
semantic target cannot be honestly reduced to rules alone, such as condescension, signal
grounding, and next-step quality.

## 5. Uses

### Intended uses

- Train a small preference-tuned judge or critic for Tenacious-specific outreach review.
- Run regression checks on candidate outputs after prompt, routing, or policy changes.
- Compare prompt-only evaluation against judge-assisted evaluation on a sealed held-out split.

### Out-of-scope or inappropriate uses

- Real prospecting or production outreach generation.
- Generic sales-email training outside the Tenacious setting.
- Training on `held_out` or evaluating systems that have already seen the sealed split.

### Key limitations

- The corpus is authored and reconstructed, not sampled from a production outreach stream.
- Synthetic coverage is intentionally limited and still far below the full target mix.
- SMS coverage is thin.
- The held-out split now meets the 50-task target, but the human reliability workflow is still
  incomplete.

## 6. Distribution

**Canonical files.**

- `tenacious_bench_v0.1/train/*.jsonl`
- `tenacious_bench_v0.1/dev/*.jsonl`
- local sealed `tenacious_bench_v0.1/held_out/*.jsonl` (not versioned in git)

`*_prompt_manifest.jsonl` files are generation artifacts, not benchmark rows.

**Access policy.** `train` and `dev` are the intended sharable benchmark surfaces. `held_out` is
maintained locally in this workspace, remains gitignored by repo policy, and is not versioned in
git. It must stay sealed from training and public scoring claims.

**License.** CC-BY-4.0, matching the PRD acceptance criteria for public dataset release.

## 7. Maintenance

**Maintainer.** Nebiyou Abebe, 10 Academy TRP1 Week 11.

### Update policy

Changes to the benchmark should preserve:

- schema validity,
- held-out separation,
- provenance fields in `metadata`,
- model-family rotation between synthetic generation and synthetic judging,
- reproducibility metadata such as prompt version and generation seed.

### Known gaps

- `synthetic` coverage is 11 tasks today, so the corpus remains programmatic and trace-derived
  heavy.
- `sms` coverage is 9 tasks, which under-represents that channel.
- `hand_authored` coverage is concentrated in `train` and `held_out`; `dev` currently has no
  hand-authored rows.
- The human reliability workflow in `docs/inter_rater_agreement.md` is still pending, so the
  benchmark is sealed and contamination-checked but not yet fully human-calibrated.

### Version notes

- `v0.1-wave1`: initial committed benchmark skeleton.
- `v0.1-wave2`: corpus expanded to the 200-task planning threshold for `train` + `dev`.
- `v0.1-wave4`: 211 public authoring rows plus 14 sealed held-out rows, with live synthetic
  generation accepted into `train` and `dev`.
- `v0.1-act2-hardening`: 211 public authoring rows plus 50 sealed held-out rows, with preference
  prep hardened so held-out rows are not indexed by training utilities.
