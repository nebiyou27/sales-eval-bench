# Tenacious-Bench v0.1 — Evaluation Memo
**Path B: ORPO Preference-Tuned Critic (Qwen3-0.6B LoRA)**
Nebiyou Abebe · May 2026

---

## Page 1 — Deployment Decision

### Executive Summary

Tenacious-Bench v0.1 is a 261-task benchmark targeting the two dominant Week 10 failure modes —
P33 gap-condescension (15.6% A/B incident rate) and P24 AI-maturity empty JSON (43.3% tau2
incident rate) — evaluated against a Qwen3-0.6B LoRA adapter trained via ORPO on 211 preference
pairs. Live inference on the 50-task held-out set shows the trained adapter achieving a **26%
pass rate vs. 12% for the prompt-only baseline (Delta B = +14 pp)**. The lift is in the positive
direction but is not statistically significant at n=50 (p=0.23, 95% CI: −2 to +30 pp). Delta A
vs. the Week 10 baseline cannot be computed because the baseline prediction file does not contain
matching held-out task IDs. The recommendation is **do not deploy yet** — the training signal is
directionally real but underpowered; the path to deployment is more data and more epochs, not a
different algorithm.

---

### Delta A — Trained vs. Week 10 Baseline

**Status: Not computable.**

The Week 10 baseline predictions file does not contain task IDs matching the held-out set. Delta A
will require re-running Week 10 baseline inference against the current held-out task IDs before
a valid cross-system comparison can be reported. This is a measurement gap, not a negative result.

---

### Delta B — Prompt-Only Baseline (Same Backbone)

| System | Held-out pass rate (n=50) |
|---|---|
| Trained LoRA (Qwen3-0.6B) | 26% (13/50) |
| Prompt-only (Qwen3-0.6B, no LoRA) | 12% (6/50) |
| **Delta B** | **+14 pp** |

**Statistical summary:** Paired bootstrap, n=2000 resamples.
Score-level: mean Δ = +0.033, 95% CI (−0.019, +0.086), p = 0.2329.
Pass-rate-level: mean Δ = +0.14, 95% CI (−0.02, +0.30).

**Interpretation:** Delta B is positive — the trained adapter outperforms the bare backbone on
the held-out distribution. The confidence interval straddles zero, so the result does not meet
the p < 0.05 threshold for a claimed training contribution. This is an underpowered positive
result, not a null result. The distinction matters: the previous stub-run reported a negative
Delta B (−6 pp); live inference reversed that direction. The most likely explanation is that 211
preference pairs and 1 epoch produced a real but small behavioral shift that n=50 tasks cannot
resolve at standard significance thresholds. The correct next step is more data, not a different
algorithm.

---

### Cost Per Task

| System | Avg latency / task | Avg cost / task |
|---|---|---|
| Prompt-only (Qwen3-0.6B) | 14,045 ms | $0.00* |
| Trained LoRA (Qwen3-0.6B) | 14,228 ms | $0.00* |
| **Latency delta (trained vs prompt-only)** | **+183 ms (+1.3%)** | — |

*Cost is $0.00 because inference ran on a free Colab T4. At standard cloud GPU rates
(e.g., $0.35/hr for a T4), 14.2 s per task implies approximately $0.0014/task for both systems —
the adapter adds negligible latency overhead after merge-and-unload.

**Production implication:** The latency concern from the stub run (+79%) does not exist in live
inference. The adapter merge-and-unload is a one-time cost at load time; per-task inference is
essentially identical between trained and prompt-only modes. The latency deployment gate
(18,000 ms) is already met by both systems.

---

### Production Recommendation

**Recommendation: Do not deploy yet — revisit after retraining.**

The trained component shows a directionally positive signal (Delta B = +14 pp) with negligible
latency cost (+1.3%). The blocker is statistical power, not direction. Three conditions must be
met before deployment:

1. **Statistical significance gate:** Delta B must reach p < 0.05 on the held-out set. The
   current result (p=0.23) requires approximately 150–200 held-out tasks or a larger behavioral
   shift from retraining to cross the threshold at n=50.

2. **Delta A measurement:** Week 10 baseline inference must be re-run against the current
   held-out task IDs to produce a valid cross-system comparison.

3. **Retraining with more contrastive pairs:** The loss plateau at ~4.4 suggests the current
   preference pairs are insufficiently contrastive. Retraining with sharper chosen/rejected
   pairs (rubric-failing phrases in rejected, not just syntactic variants) is likely to produce
   a larger behavioral shift that resolves at n=50.

If conditions 1 and 2 are met after retraining, re-classify to **deploy with caveat** with a
minimum 14-day live monitoring window before unconditional deployment.

---

## Page 2 — Benchmark Limitations and Forward Plan

### Tenacious-Bench v0.2 — Missing Coverage Gaps

The following four failure modes have **zero tasks** in v0.1. Each describes behavior the
current benchmark cannot grade because no task targets it.

**Gap 1 — Multi-turn follow-up consistency (P34, unmeasured)**
No v0.1 task tests whether the agent contradicts claims made in a prior thread message when
composing a follow-up. The bench grades single-message outputs only; a follow-up that
re-introduces a gap-condescension framing that was absent in the opener passes the rubric even
though the full thread is now P33-triggering.
*v0.2 addition:* A `prior_thread` follow-up partition with paired opener + follow-up tasks
where the rubric scores the delta between messages, not each message in isolation.

**Gap 2 — Bench-capacity over-commitment (P32, unmeasured)**
No v0.1 task tests whether the agent promises delivery capacity beyond what the `bench_context`
field allows. The rubric scores tone and citation but does not check whether the capacity claim
in the body is arithmetically consistent with `bench_context.capacity_commitment_allowed` and
`pricing_scope` for multi-stack scenarios.
*v0.2 addition:* A `capacity_arithmetic` deterministic dimension that parses the body for
numeric capacity commitments and fails the task if the claimed headcount or timeline exceeds
what the bench context permits.

**Gap 3 — Multi-contact account framing consistency (P35, unmeasured)**
No v0.1 task tests framing consistency across two contacts at the same account — e.g., a
technical contact and an economic buyer receiving outreach in the same week. The current bench
treats each message in isolation; it cannot detect when the agent gives conflicting AI-maturity
scores or different gap framings to two contacts at the same company.
*v0.2 addition:* Paired-contact task groups where both messages share the same `prospect.company_name`
and the rubric verifies that the `ai_maturity.score` and `failure_dimension` framing are
consistent across the pair.

**Gap 4 — Warm-intro acknowledgment and tone shift (P22, unmeasured)**
No v0.1 task tests the case where `prior_thread.contacted_before = true` and a named referral
exists. The bench scores the CTA and signal citation but does not verify that the agent
acknowledges the prior contact or adjusts tone away from cold-outreach register. An agent that
ignores a warm intro and pitches as if the contact is cold passes all current rubric dimensions.
*v0.2 addition:* A `warm_intro_acknowledgment` rubric dimension, active when
`prior_thread.contacted_before = true`, that fails any draft that does not reference the prior
interaction or that uses cold-open language (e.g., "I came across your company" variants flagged
as `forbidden_terms`).

---

### Ground Truth Faithfulness Self-Critique

The rubric's `signal_grounding` dimension scores whether the body cites a hiring signal and
assigns that citation a confidence tier consistent with `hiring_signal_brief.signal_confidence`.
The ground-truth labels were derived from public hiring data (LinkedIn, Builtwith stack
inferences) at the time of dataset authoring.

**Specific lossiness mechanism:** Hiring signals lag actual stack decisions by four to twelve
weeks. A signal logged as `confidence: high` at authoring time may reflect a hiring wave that
has already closed by the time the outreach is scored. The rubric rewards any body that cites
the signal and tiers it correctly — it cannot penalize a citation that is factually stale because
the ground truth was frozen at authoring time, not at notional send time. This lossiness
**systematically over-rewards signal-grounding**: an output that cites the exact signal from
`hiring_signal_brief` receives full `signal_grounding` credit regardless of whether that signal
is still actionable. The practical effect: the true production pass rate for `signal_grounding`
dimensions is likely lower than what Delta B reports.

---

### Unresolved Training Issue

**Issue: Loss plateau at ~4.4 with no convergence below 4.3 across 53 training steps.**

The ORPO run completed 53 gradient steps (1 epoch, batch size 1, gradient accumulation 4,
effective batch 4) on 211 preference pairs. Loss started at 5.02 and declined to approximately
4.36 by step 10, then stalled. Despite this, Delta B is positive (+14 pp), which suggests the
early gradient steps produced a real behavioral shift even without full convergence.

The stall pattern is consistent with insufficiently contrastive preference pairs: the `chosen`
and `rejected` outputs were constructed from the same task templates with small lexical edits,
meaning the log-odds margin was narrow after the first few steps.

**What would be tried next:** (1) Increase ORPO beta from 0.1 to 0.3 to sharpen the preference
margin penalty. (2) Run 3 epochs rather than 1. (3) Reconstruct chosen/rejected pairs so
rejected outputs contain at least one rubric-failing phrase from the banned list rather than
syntactically varied but semantically similar reformulations. This is a training-data
contrastiveness failure — more epochs alone will not resolve it.

---

### Kill-Switch Trigger Condition

The trained component is a preference-tuned critic (Path B) — its role is to approve or reject
candidate outreach drafts before send. The relevant failure signal is **false-approval rate**:
the fraction of drafts the critic approves that are subsequently flagged as P33 or P24 failures
by a human reviewer.

**Trigger condition:** If the false-approval rate over a rolling 7-day production window exceeds
**30%** of approved sends, the LoRA adapter is disabled and inference falls back to the
prompt-only Qwen3-0.6B baseline.

**Justification:** The 30% threshold is calibrated against the pre-trained baseline incident
rates: P33 at 15.6% and P24 at 43.3% give a combined observed failure rate of approximately
29% on the hardest task types. A trained critic allowing more than 30% of its approvals to be
failures provides no production value over the uncontrolled baseline.

**Observable metric:** Any outreach flagged by the human operations reviewer as containing
gap-condescension language (P33) or an invalid AI-maturity claim (P24) within 48 hours of send
is counted as a false approval. Observable in production without a held-out re-run.

**Action on trigger:** Disable the LoRA adapter, revert to prompt-only Qwen3-0.6B, and open
a data-collection window to capture new P33/P24 failure instances as additional preference pairs
for the next training run.
