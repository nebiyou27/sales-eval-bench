# Tenacious-Bench v0.1 — Datasheet

Follows Gebru et al. (2021) seven-section structure with Pushkarna-style layered detail
(telescopic summary → periscopic structure → microscopic field/schema detail).

---

## 1. Motivation

**Telescopic summary.** Tenacious-Bench v0.1 is a machine-verifiable benchmark for evaluating
the Tenacious Week 10 Conversion Engine on the two failure modes that caused 100% of observed
Delta-A degradation: gap-condescension (P33, 15.6% A/B trigger rate) and AI-maturity
inconsistency (P24, 43.3% τ²-run incident rate).

**Periscopic structure.** The benchmark supports:
- Deterministic scoring without human input (12 rule-based dimensions per task)
- ORPO preference-pair generation for LoRA fine-tuning (Path B)
- Ablation studies comparing judge-only vs. trained-critic evaluation on held-out tasks

**Who created this and why?** Nebiyou Abebe (10 Academy TRP1) created this dataset as part of
Week 11 to support training a LoRA-based judge that catches the P24 and P33 failure modes
before outreach is sent. The immediate use case is Tenacious internal quality assurance.

**Funding.** No external funding. Total projected API spend ≤ $5 (dev-tier models only).

---

## 2. Composition

**Telescopic summary.** 200 machine-verifiable B2B outreach tasks across 3 partitions, covering
6 failure dimensions, 3 difficulty levels, 3 channels, 3 message kinds, and 4 source modes.

**Periscopic structure.**

### Partition counts

| partition | count | % of total |
|---|---|---|
| train | 125 | 62.5% |
| dev | 75 | 37.5% |
| held_out | 4 (partial) | sealed, gitignored |
| **total (train+dev)** | **200** | |

Target is 250 total (train 125 / dev 75 / held_out 50). Train and dev targets are met;
held_out expansion to 50 is planned for Wave 4 before the May 3 deadline.

### By failure_dimension

| failure_dimension | train | dev | total (train+dev) | target (train+dev) |
|---|---|---|---|---|
| `gap_condescension` (P33) | 25 | 14 | 39 | 40 |
| `ai_maturity_consistency` (P24) | 25 | 14 | 39 | 40 |
| `output_validity` | 22 | 14 | 36 | 32 |
| `signal_grounding` | 17 | 8 | 25 | 31 |
| `style_guide_adherence` | 22 | 17 | 39 | 30 |
| `next_step_quality` | 14 | 8 | 22 | 27 |
| **Total** | **125** | **75** | **200** | **200** |

P24 and P33 — the two primary failure-mode dimensions — hit exact targets in train (25 each)
and are within 1 of target in dev. Minor redistribution occurred because programmatic blueprints
cover multiple dimensions per blueprint.

### By source_mode

| source_mode | train | dev | total | target (full corpus) |
|---|---|---|---|---|
| `programmatic` | 72 | 51 | 123 | 75 |
| `trace_derived` | 36 | 24 | 60 | 50 |
| `hand_authored` | 17 | 0 | 17 | 25 |
| `synthetic` | 0 | 0 | 0 | 100 |
| **Total** | **125** | **75** | **200** | **250** |

Synthetic mode (target 100) requires live API calls and is scheduled for Wave 4 (Days 4–6).
Programmatic and trace_derived are over their per-mode targets because they filled the synthetic
gap for the interim submission.

### By difficulty

| difficulty | train | dev | total |
|---|---|---|---|
| hard | 58 | 28 | 86 |
| medium | 34 | 22 | 56 |
| easy | 33 | 25 | 58 |

Hard skew reflects the methodology requirement to weight P24/P33 at 1.25× standard allocation
and to prioritise hard difficulty where both failures originate.

### By channel

| channel | train | dev | total | target (train+dev) |
|---|---|---|---|---|
| email | 86 | 48 | 134 | 150 |
| linkedin_dm | 37 | 21 | 58 | 75 |
| sms | 2 | 6 | 8 | 25 |

SMS is under target (8/25) because programmatic blueprints conservatively limit sms variants
to warm_reply only per P12–P15 channel safety constraints. SMS will be expanded in Wave 4.

### By message_kind (train+dev)

| message_kind | count |
|---|---|
| warm_reply | 89 |
| cold_outreach | 71 |
| reengagement | 40 |

**Microscopic field/schema detail.** Each task is a JSON object conforming to `schema.json`
(Draft 2020-12). Required top-level fields: `task_id`, `partition`, `source_mode`, `difficulty`,
`failure_dimension`, `channel`, `message_kind`, `input`, `candidate_output`, `ground_truth`,
`rubric`, `scoring_config`, `metadata`. The `input` object contains `prospect` (company, role,
stage), `hiring_signal_brief` (segment, confidence, signals array, ai_maturity), `bench_context`
(supported_stacks, pricing_scope), and `prior_thread` (contacted_before, summary). The
`candidate_output` contains `body` and (for email) `subject`. The `rubric` specifies
`expected_terms`, `forbidden_terms`, `banned_phrases`, `max_body_words`, and tone markers.
`scoring_config.deterministic_dimensions` lists the checks to run without human input.

---

## 3. Collection Process

**Telescopic summary.** Tasks were created using four authoring modes: trace_derived (from
audited Week 10 failure traces), programmatic (deterministic blueprint expansion), hand_authored
(explicit adversarial seeds), and synthetic (offline prompt manifests; live generation pending).

**Periscopic structure.**

### trace_derived (60 tasks)
Source: `seed/trace_log.jsonl` — 41 Week 10 simulation records with `reward=0.0`. Blueprints
assign failure_dimension, difficulty, expected_terms, and other rubric parameters. Each trace ID
is checked against `seed/held_out_traces.jsonl` to prevent leakage. Original prompt/output
payloads are not copied into the repo; only trace metadata (simulation_id, reward, domain,
termination_reason) is used as provenance.

### programmatic (123 tasks)
12 blueprints each define a failure scenario with 3 evidence templates, 3 ask templates,
3 subject stems, and 2 prior-thread templates. The `materialize_tasks()` function in
`src/generation/generate_programmatic.py` expands each blueprint across a prospect list using
round-robin selection. No LLM calls are made; all text is deterministic.

### hand_authored (17 train + 4 held_out)
Specs in `src/generation/generate_hand_authored.py`. Each task was authored against a specific
Week 10 probe (P03, P07, P10, P12, P19, P24, P25, P26, P29, P30, P31, P32, P33, P34, P35).
Hard-difficulty tasks were deliberately designed with adversarial constraints (expert buyer,
conflicting signals, duplicate-send state) to maximise ORPO training signal for the most
challenging cases.

### synthetic (0 live tasks, 3 dev manifests)
`src/generation/generate_synthesis.py` produces offline prompt manifests for review. Live
generation (Qwen3-Next-80B generator + DeepSeek V3.2 judge, R2 rotation) is scheduled for
Wave 4. All live calls will be logged to `cost/log.csv`.

**Data freshness.** All seed traces are from Week 10 (April 2026) Tenacious Conversion Engine
runs. No live prospect data is used; all company names and contacts are fictional.

---

## 4. Preprocessing, Cleaning, and Labeling

**Telescopic summary.** Tasks pass three validation layers before entering a partition: schema
validation (jsonschema Draft 2020-12), held-out leakage check, and contamination check
(8-gram overlap + lexical cosine + MiniLM embedding cosine vs. held-out partition).

**Preprocessing steps:**
1. `validate_task()` in `common.py` — schema validation against `schema.json`
2. `assert_no_held_out_leakage()` — blocks any task citing a seed held-out trace ID
3. `contamination_check.py` — 8-gram overlap (threshold: any shared gram), lexical cosine
   (threshold: ≥0.85), embedding cosine (threshold: ≥0.93) between held_out and train+dev

**Labeling.** `ground_truth.target_decision` is assigned by the blueprint author based on
whether the `candidate_output` demonstrates correct behaviour (accept), a correctable failure
(revise), or an unacceptable output (block). All current train/dev tasks have
`target_decision=accept` — they are positive examples of correct outreach. Negative examples
(rejected pairs for ORPO) will be generated via the synthesis pipeline in Wave 4.

**Deterministic scoring.** The `scoring_evaluator.py` evaluates 12 binary dimensions against
the candidate_output without calling an LLM. Failing a deterministic dimension means the task's
rubric is misconfigured and the task must be corrected before entering the corpus.

---

## 5. Uses

**Intended uses:**
- Training a Qwen3-0.6B ORPO LoRA judge (Path B) to catch P24 and P33 failures
- Ablation studies comparing judge-trained model vs. prompt-only baseline on held-out split
- Regression testing of the Tenacious Conversion Engine after updates

**Inappropriate uses:**
- Production prospect outreach (all company names are fictional)
- Generic sales outreach training outside the Tenacious context
- Evaluating systems that have seen the held_out partition during training

**Limitations:**
- All tasks are authored, not collected from real outreach; the distribution may not match
  the full long-tail of real prospect interactions
- Synthetic Wave (40% of target) has not been generated yet; current corpus is
  programmatic/trace_derived-heavy
- held_out partition is partial (4/50 target); ablation results will be preliminary until
  held_out is fully populated

---

## 6. Distribution

**Access.** The train and dev partitions will be published to HuggingFace datasets under
the project account before the May 3 deadline. The held_out partition is gitignored and will
not be publicly released.

**License.** Apache 2.0 (matching the Tenacious Conversion Engine repo).

**Export.** `tenacious_bench_v0.1/train/*.jsonl`, `tenacious_bench_v0.1/dev/*.jsonl` are the
canonical files. Each line is a self-contained JSON task conforming to `schema.json`.

---

## 7. Maintenance

**Maintainer.** Nebiyou Abebe (nebiyoua@10academy.org), 10 Academy TRP1 Week 11.

**Updates planned:**
- Wave 4 (before May 3): synthetic tasks via live API (Qwen3-Next-80B + DeepSeek V3.2 judge),
  held_out expansion to 50 tasks, ORPO preference pairs
- Post-training: ablation results logged to `docs/inter_rater_agreement.md`

**Known issues:**
- `signal_grounding` (25 tasks) and `next_step_quality` (22 tasks) are below methodology
  targets in train+dev. Synthetic Wave will close these gaps.
- SMS channel is under-represented (8/25 target). Wave 4 will add SMS-specific synthetic tasks.
- `hand_authored` mode is at 17/25 target; 8 more hand-authored tasks are needed for Wave 4.

**Version history:**
- v0.1-wave1: 122 tasks (train 74, dev 48) — Apr 29 2026
- v0.1-wave2: 200 tasks (train 125, dev 75) — Apr 30 2026
