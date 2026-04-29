# Methodology - Tenacious-Bench v0.1

## Path Declaration

**Path B - Preference-tuned judge / critic**

### Justification

Week 10 evidence points to two dominant failure modes:

1. **P33 - Gap-condescension** (15.6% trigger rate, A/B n=32 signal-grounded drafts): the
   agent generates an output but cannot detect when its language is presumptuous or intrusive
   toward sophisticated buyers. The sensitivity axis in `agent/claims/sensitivity.py` flags the
   claim kind but does not prevent the generation from proceeding with inappropriate confidence.
   Evidence source: `D:\TRP-1\week-10\Conversion Engine\eval\ab_reply_rate_report.json`,
   run `ab-reply-rate-a4`, rejected signal-grounded drafts:
   `contradicted-co:trial-4`, `contradicted-co:trial-7`,
   `shadow-startup:trial-2`, `shadow-startup:trial-6`,
   `silent-sophisticate:trial-5`.

2. **P24 - AI-maturity inconsistency** (43.3% incident rate, tau2 n=30 thinking-model tasks): the
   agent produces empty or invalid JSON on hard AI-maturity tasks and cannot self-identify the
   failure. The system scores it as a pass internally while the output is unusable.
   Evidence source: `seed/held_out_traces.jsonl`, tau2 dev-slice run
   `conversion_engine_treatment`, reward-0.0 task IDs:
   `2ee84e7e-ebcb-4006-a066-1c9d373fc99f` (task 1),
   `d174d025-936f-49e7-8183-1497f8bac193` (task 7),
   `f5497551-5989-48a6-9c14-ac73106044ae` (task 52),
   `ba85025f-496d-43c0-91ed-39de2e2e480d` (task 66).

Week 10 held-out traces are cited as Path B justification only; Week 11 train/dev partitions
exclude these trace IDs. They may appear in audit evidence and methodology rationale, but they
must not be copied into preference pairs, task inputs, candidate outputs, or any generated
train/dev examples.

Both are **inconsistency failures**: the agent is right most of the time but has no mechanism
to catch when it is wrong. A trained judge/critic (Path B) is the correct treatment. A
generation fix (Path A) would only improve average output quality; it would not add
self-detection. A PRM (Path C) requires multi-turn trajectory data we do not have at scale.

### Algorithm Choice

**ORPO** (Hong, Lee, and Thorne, EMNLP 2024) over DPO or SimPO.

Rationale: ORPO is reference-model-free and combines supervised fine-tuning with preference
alignment in a single training objective. This is the property formalized in Hong et al.,
Section 3, especially the odds-ratio objective in Eq. 6 and the combined ORPO objective that
adds the SFT loss to the odds-ratio penalty. This matters for Week 11 because the training
budget is small and the default runtime is Colab T4. The training data naturally fits ORPO:
each example can be represented as a chosen Tenacious-compliant output and a rejected unsafe,
unsupported, invalid, or off-tone output.

DPO is the foundational preference-optimization baseline, but it is less attractive for this
project because it requires maintaining a reference policy during training. SimPO is also
reference-free and strong, but its average-log-probability reward and length-related calibration
are less convenient for short sales-outreach and JSON-validity tasks. ORPO gives the cleanest
implementation story for a small preference-tuned critic.

---

## Rubric And Scoring

The benchmark rubric is machine-verifiable first. The target semantic dimensions are
`output_validity`, `ai_maturity_consistency`, `gap_condescension`, `signal_grounding`,
`style_guide_adherence`, and `next_step_quality`. Each task stores executable scoring rules in
`schema.json`; `src/scoring/scoring_evaluator.py` is the forward-compatible command path for local
scoring, deterministic checks, and any judge-backed score fields that cannot be reduced to a
regex or JSON-schema constraint.

The Day Zero evaluator exposes only honest deterministic smoke checks:
`output_nonempty`, `ai_maturity_keyword_present`, `banned_condescension_absent`,
`expected_signal_term_present`, `forbidden_terms_absent`, and
`buyer_next_step_keyword_present`. These checks verify wiring and obvious failures; they do not
claim to fully score semantic consistency or buyer-fit quality until the Day 1 rubric is tightened.

Judge-backed score fields are run with temperature 0, fixed seed where the provider supports it,
and an explicitly pinned model/version string in the run manifest, for example
`deepseek-v3.2-exp@YYYY-MM-DD`. A run is invalid if the judge model changes mid-pass without a
new run ID.

`next_step_quality` is scored as a hybrid field: deterministic checks first verify that the output
contains an explicit buyer-facing next step or CTA, while the judge-backed scorer rates specificity
and fit on a 1-5 scale. The dimension passes only when the deterministic CTA check passes and the
specificity score is at least 4/5.

---

## Partitioning Protocol

| Partition | Share | Size (target) | Use |
|---|---|---|---|
| `train/` | 50% | ~125 tasks | LoRA training |
| `dev/` | 30% | ~75 tasks | Iteration, rubric calibration |
| `held_out/` | 20% | ~50 tasks | Sealed evaluation only |

Held-out is sealed after contamination checks pass. It is gitignored from training scripts and
not committed in unencrypted form until the leaderboard is published.

Delta A is tested on the paired held-out set with McNemar's test for binary pass/fail and a
paired bootstrap 95% CI over task-level score deltas. With n=50, a 10 percentage point lift is
reported as directional unless its paired CI clears zero; the target minimum detectable effect is
approximately 20-25 percentage points at alpha=0.05 under conservative discordance assumptions,
assuming roughly 30% discordant pairs.

---

## Contamination Protocol

Three checks before any task enters the held-out partition:

1. **N-gram overlap** - less than 8-gram overlap on input fields between held-out and training,
   following the PaLM-style 8-gram decontamination convention for benchmark/train overlap.
2. **Embedding similarity** - cosine similarity below 0.85 between held-out and training tasks
   using `all-MiniLM-L6-v2`. Scores at or above 0.85 are treated as near-duplicate candidates,
   matching common RAG and eval decontamination practice; borderline cases are manually removed
   or rewritten before sealing. The current code attempts this pass through the local
   `transformers` stack first, preferring the repo-local snapshot at
   `models/embeddings/all-MiniLM-L6-v2/`. The bootstrap command is
   `python src/generation/fetch_embedding_model.py`. If the required weights are still absent,
   the report emits an explicit unavailable-model status instead of claiming semantic
   decontamination succeeded.
3. **Time-shift verification** - any task referencing public signal (layoffs, job posts, funding)
   must include a machine-checkable `retrieval_provenance` field with `url`, `retrieved_at`
   (ISO-8601 UTC), and `source_type`.

Results are written to `src/generation/contamination_check.json`. A report only counts as a full
embedding-backed pass when `embedding_check_status=embedding_check_completed`; fallback statuses are
honest scaffolding states, not evidence that semantic decontamination is fully closed.

---

## Multi-LLM Routing Policy

To prevent preference leakage (Li et al., 2025), model families are rotated:

| Role | Model | Budget tier |
|---|---|---|
| Hand-authored hard seeds | Human-authored from Week 10 probes | free |
| Optional hard-seed expansion | Claude/GPT-class frontier model | eval-tier, limited and logged |
| Bulk variation generation | Qwen3-Next-80B via OpenRouter | dev-tier |
| Judge filtering | DeepSeek V3.2 via OpenRouter | dev-tier |
| Calibration spot-check | Claude/GPT-class frontier model | eval-tier, max 50 tasks |
| Chosen-rewrite for preference pairs | Qwen3-Next-80B or another non-judge family | dev-tier |

The same model is never used to generate and judge the same task. This policy is now enforced in
code for the synthesis path through `src/generation/synthesis_policy.py`. Chosen rewrites are
first screened by `src/scoring/scoring_evaluator.py`; any LLM score used for acceptance must come
from a different model family than the rewrite generator. DeepSeek may filter Qwen-generated bulk
variants, but a DeepSeek-generated rewrite cannot be accepted by a DeepSeek-only judge pass.

For the R4 audit trail, every synthesis, judge, calibration, training, smoke-test, and held-out
evaluation call is logged to `cost/log.csv` with timestamp, role, model/version, input tokens,
output tokens, and USD cost.

### Synthetic Data Quality Gate

The Day 0 reading memo in `docs/memos/synthetic_data_best_practices_v0.md` sets the
dataset-authoring rule for Acts II-III: synthetic examples must be controlled, metadata-rich,
and filtered before partition assignment. Bulk generation should start from probe and
trace-derived templates, preserve provenance in `metadata`, and pass deterministic checks before
any model-family-rotated judge score is trusted. This keeps the benchmark focused on
Tenacious-specific failures rather than generic sales-writing quality.

---

## Human Reliability Protocol

### Test-Retest Reliability

One labeler hand-labels a 30-task subset against the rubric, then re-labels the same subset
24 hours later without reference to first labels. The matrix is committed to
`docs/inter_rater_agreement.md` under a `test_retest` section.

Threshold: Cohen's kappa >=0.6 on each rubric dimension before the held-out is sealed, with raw
percent agreement reported alongside kappa for readability. If any dimension drops below kappa
0.6, sealing pauses; the dimension is rewritten into stricter observable criteria, the 30-task
subset is re-labeled, and the failing dimension is dropped from Delta A if it cannot clear the
threshold after one revision.

### Inter-Rater Reliability

A second labeler independently labels a 30-task subset sampled from the same calibration pool
using uniform random sampling with a fixed seed.
Agreement is reported separately in `docs/inter_rater_agreement.md` under an `inter_rater` section.
Threshold: Cohen's kappa >=0.6 on every human-reviewed rubric dimension before the held-out is
sealed, with raw agreement and Wilson 95% CI reported for each dimension. Disagreements are
adjudicated into rubric edits only; adjudicated labels do not replace the original labels used to
report agreement.
