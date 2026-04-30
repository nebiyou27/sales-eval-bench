# Inter-Rater Agreement — Tenacious-Bench v0.1

Generated: Apr 30 2026. Covers a 30-task stratified subset drawn from the dev partition.

Status note: the sealed `held_out` split now reaches 50 tasks and passes contamination, but the
human reliability workflow documented here is still pending. Act II hardening is complete on split
size and contamination control; Act III should still treat human agreement as unfinished work.

---

## Subset Composition

5 tasks per failure dimension, stratified across difficulty levels and source modes.

| # | task_id | failure_dimension | difficulty | source_mode |
|---|---|---|---|---|
| 1 | dev-programmatic-013-competitor-gap-research-frame | gap_condescension | hard | programmatic |
| 2 | dev-programmatic-016-competitor-gap-research-frame | gap_condescension | hard | programmatic |
| 3 | dev-trace-derived-001-competitor-gap-restraint | gap_condescension | hard | trace_derived |
| 4 | dev-trace-derived-004-competitor-gap-restraint | gap_condescension | hard | trace_derived |
| 5 | dev-programmatic-033-leadership-gap-frame | gap_condescension | medium | programmatic |
| 6 | dev-programmatic-001-ai-maturity-structured-reply | ai_maturity_consistency | hard | programmatic |
| 7 | dev-programmatic-004-ai-maturity-structured-reply | ai_maturity_consistency | hard | programmatic |
| 8 | dev-trace-derived-007-ai-maturity-structured-visibility | ai_maturity_consistency | hard | trace_derived |
| 9 | dev-trace-derived-010-ai-maturity-structured-visibility | ai_maturity_consistency | hard | trace_derived |
| 10 | dev-programmatic-037-maturity-score-conservative | ai_maturity_consistency | easy | programmatic |
| 11 | dev-programmatic-021-output-clean-abstain | output_validity | easy | programmatic |
| 12 | dev-programmatic-024-output-clean-abstain | output_validity | easy | programmatic |
| 13 | dev-trace-derived-019-thin-evidence-restraint | output_validity | easy | trace_derived |
| 14 | dev-trace-derived-022-thin-evidence-restraint | output_validity | easy | trace_derived |
| 15 | dev-programmatic-041-reengagement-format-check | output_validity | medium | programmatic |
| 16 | dev-programmatic-005-thin-signal-restraint | signal_grounding | easy | programmatic |
| 17 | dev-programmatic-008-thin-signal-restraint | signal_grounding | easy | programmatic |
| 18 | dev-programmatic-025-pricing-scope-boundary | signal_grounding | hard | programmatic |
| 19 | dev-programmatic-027-pricing-scope-boundary | signal_grounding | hard | programmatic |
| 20 | dev-programmatic-028-pricing-scope-boundary | signal_grounding | hard | programmatic |
| 21 | dev-programmatic-009-fixture-live-boundary | style_guide_adherence | medium | programmatic |
| 22 | dev-programmatic-012-fixture-live-boundary | style_guide_adherence | medium | programmatic |
| 23 | dev-trace-derived-013-demo-boundary-honesty | style_guide_adherence | medium | trace_derived |
| 24 | dev-trace-derived-016-demo-boundary-honesty | style_guide_adherence | medium | trace_derived |
| 25 | dev-programmatic-045-style-prefix-explicit | style_guide_adherence | easy | programmatic |
| 26 | dev-programmatic-017-timezone-aware-next-step | next_step_quality | medium | programmatic |
| 27 | dev-programmatic-020-timezone-aware-next-step | next_step_quality | medium | programmatic |
| 28 | dev-programmatic-029-capacity-gate-first | next_step_quality | hard | programmatic |
| 29 | dev-programmatic-030-capacity-gate-first | next_step_quality | hard | programmatic |
| 30 | dev-programmatic-032-capacity-gate-first | next_step_quality | hard | programmatic |

---

## test_retest

### First-Pass Labels (Apr 30 2026)

Labeler: `scoring_evaluator.py` (deterministic rule engine, version committed at wave-2 tag).
All 30 tasks in the subset are positive examples (`target_decision=accept`).
Each cell records the fraction of tasks in that row-group that received a `1.0` on each dimension.

**Deterministic dimensions — first pass**

| # | task_id | nonempty | subj_email | body_wc | subj_chars | ai_kw | no_banned | no_bench | no_cond | signal_term | no_forbid | cta_kw | single_ask | overall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | dev-programmatic-013 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 2 | dev-programmatic-016 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 3 | dev-trace-derived-001 | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 4 | dev-trace-derived-004 | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 5 | dev-programmatic-033 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 6 | dev-programmatic-001 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 7 | dev-programmatic-004 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 8 | dev-trace-derived-007 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 9 | dev-trace-derived-010 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 10 | dev-programmatic-037 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 11 | dev-programmatic-021 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 12 | dev-programmatic-024 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 13 | dev-trace-derived-019 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 14 | dev-trace-derived-022 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 15 | dev-programmatic-041 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 16 | dev-programmatic-005 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 17 | dev-programmatic-008 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 18 | dev-programmatic-025 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 19 | dev-programmatic-027 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 20 | dev-programmatic-028 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 21 | dev-programmatic-009 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | PASS |
| 22 | dev-programmatic-012 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | PASS |
| 23 | dev-trace-derived-013 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | PASS |
| 24 | dev-trace-derived-016 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | PASS |
| 25 | dev-programmatic-045 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 26 | dev-programmatic-017 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | PASS |
| 27 | dev-programmatic-020 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | PASS |
| 28 | dev-programmatic-029 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 29 | dev-programmatic-030 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| 30 | dev-programmatic-032 | ✓ | — | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |

**Key:** `—` = dimension not included in task's `scoring_config.deterministic_dimensions`
(not applicable for that channel/dimension), not a failure. `✓` = scored 1.0.

**Summary by dimension (first pass)**

| dimension | applicable tasks | pass | fail | pass_rate |
|---|---|---|---|---|
| output_nonempty | 30 | 30 | 0 | 100% |
| subject_present_for_email | 10 | 10 | 0 | 100% |
| max_body_words_respected | 30 | 30 | 0 | 100% |
| max_subject_chars_respected | 10 | 10 | 0 | 100% |
| ai_maturity_keyword_present | 15 | 15 | 0 | 100% |
| banned_phrase_absent | 30 | 30 | 0 | 100% |
| bench_term_absent | 30 | 30 | 0 | 100% |
| banned_condescension_absent | 30 | 30 | 0 | 100% |
| expected_signal_term_present | 30 | 30 | 0 | 100% |
| forbidden_terms_absent | 30 | 30 | 0 | 100% |
| buyer_next_step_keyword_present | 30 | 30 | 0 | 100% |
| single_ask_only | 20 | 20 | 0 | 100% |

### Second-Pass Labels

**STATUS: PENDING - scheduled for May 1 2026 (>=24h after first pass)**

Second pass will re-run `scoring_evaluator.py` against the same 30-task subset without
reference to first-pass results. Because deterministic scoring is stateless and rule-based,
the expected test-retest Cohen's kappa is 1.0 on all dimensions. Any discrepancy would indicate
a non-deterministic code path and must be investigated before the held-out split is used for
stronger ablation claims.

---

## inter_rater

**STATUS: PENDING - second labeler review scheduled before Act III calibration claims**

A second labeler will independently label the same 30-task subset using the judge dimensions
(`output_validity`, `signal_grounding`, `next_step_quality`, `gap_condescension`,
`ai_maturity_consistency`, `style_guide_adherence`) as holistic pass/fail judgments against
the task rubric.

Threshold per methodology: Cohen's kappa ≥ 0.6 on every human-reviewed dimension.
Raw agreement and Wilson 95% CI will be reported per dimension when the second-labeler pass
completes.

If any dimension falls below κ = 0.6, the dimension rubric criteria will be tightened before
the current held-out slice is used for ablation-grade reporting or expanded further.

---

## Notes

- All 30 tasks in this subset are positive examples (`target_decision=accept`). Negative
  examples (rejected pairs) will be added in Wave 4 when ORPO preference pairs are generated;
  inter-rater agreement on `target_decision` will be reported at that time.
- Deterministic dimensions are the ground truth for training signal; human-reviewed judge
  dimensions are used for ablation label validation only.
- Subset selection seed: deterministic (stratified by failure_dimension, 5 per dimension,
  ordered by task_id within each stratum).
