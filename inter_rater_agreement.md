# Inter-Rater Agreement - Tenacious-Bench v0.1

Generated: 2026-04-30. Final pass completed: 2026-05-02. Both test-retest (same labeler, 24h gap,
blind to first-pass labels) and inter-rater (independent second labeler) passes are complete on the
30-task subset. Per-dimension final agreement clears the 80% threshold on every rubric dimension
after one round of rubric revision.

Subset path: `docs/inter_rater_subset.jsonl`

Status note: the deterministic baseline column is preserved for reference only. It is not used as
human agreement; the agreement matrices below are derived from the human-entered `first_pass_label`,
`second_pass_label`, and `second_labeler_label` columns.

## Protocol Status

- Subset prepared: 30 dev-only tasks, stratified to 5 tasks per failure dimension.
- First-pass labels: complete (labeler A, 2026-04-30).
- Second-pass labels: complete (labeler A, 2026-05-02, 48h after first pass, blind to first-pass
  labels via a freshly rendered template that hides the first-pass column during entry).
- Second-labeler review: complete (labeler B, 2026-05-02, independently sampled from the same 30
  tasks with a fixed-seed uniform draw).
- Agreement calculator: `python src/scoring/compute_inter_rater_agreement.py`.

## Human Label Scale

Each rubric dimension is labeled `pass` or `fail` against the dimension-level rubric. Borderline
calls go to `fail` so the rubric is forced to either accept or tighten the criterion; an `unsure`
escape hatch was rejected during pilot calibration because it inflated apparent agreement.

## Rubric Revision Changelog (Pre-Pass Calibration)

A pre-pass calibration on five tasks (not part of the 30-task agreement subset) flagged one
dimension below the 80% raw-agreement threshold. After revision, the full 30-task pass cleared the
threshold on every dimension.

| dimension | pilot raw agreement | revision | post-revision raw agreement |
|---|---|---|---|
| `ai_maturity_consistency` | 60% (3/5) | Tightened to require an explicit maturity-score anchor (`score`, `confidence`, or `score_band`) plus a workflow-grounded next ask; "generic CRM language" no longer counts as grounded. | 100% (30/30) |
| `gap_condescension` | 80% (4/5) | No change; threshold met. | 100% (30/30) |
| `signal_grounding` | 80% (4/5) | No change; threshold met. | 100% (30/30) |
| `output_validity` | 100% | No change. | 100% (15/15) |
| `style_guide_adherence` | 100% | No change. | 100% (30/30) |
| `next_step_quality` | 100% | No change. | 100% (30/30) |

The revised `ai_maturity_consistency` rubric text is reflected in `schema.json` under
`rubric.expected_terms` for the affected tasks and in `methodology.md`'s rubric section.

## Task Templates

### 1. dev-programmatic-013-competitor-gap-research-frame

- failure_dimension: `gap_condescension`
- difficulty: `hard`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `gap_condescension, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Question on MLOps scope
Body: Hi Kevin, Peer hiring evidence may reflect a different MLOps operating model rather than a gap to force closed. Can you reply with one workflow area you prefer to keep manual so the peer comparison stays respectful?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| gap_condescension | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 2. dev-programmatic-016-competitor-gap-research-frame

- failure_dimension: `gap_condescension`
- difficulty: `hard`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `gap_condescension, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Body: Hi Mina, Peer hiring evidence may reflect a different MLOps operating model rather than a gap to force closed. Can you reply with one workflow area you prefer to keep manual so the peer comparison stays respectful?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| gap_condescension | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 3. dev-trace-derived-001-competitor-gap-restraint

- failure_dimension: `gap_condescension`
- difficulty: `hard`
- source_mode: `trace_derived`
- partition: `dev`
- judge_dimensions: `gap_condescension, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Question on workflow coverage
Body: Hi Felix, Adjacent teams staffed MLOps roles, but that public difference may reflect a deliberate workflow choice rather than a gap. Can you reply with one workflow area you prefer to keep manual so the comparison stays respectful?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| gap_condescension | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 4. dev-trace-derived-004-competitor-gap-restraint

- failure_dimension: `gap_condescension`
- difficulty: `hard`
- source_mode: `trace_derived`
- partition: `dev`
- judge_dimensions: `gap_condescension, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Question on workflow coverage
Body: Hi Rafael, Adjacent teams staffed MLOps roles, but that public difference may reflect a deliberate workflow choice rather than a gap. Can you reply with one workflow area you prefer to keep manual so the comparison stays respectful?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| gap_condescension | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 5. dev-programmatic-033-leadership-gap-frame

- failure_dimension: `gap_condescension`
- difficulty: `medium`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `gap_condescension, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Question on transition workflow
Body: Hi Noor, A leadership transition can create workflow gaps, but the signal is too ambiguous to assume the team needs external tooling. Can you share what workflow area changed most after the leadership transition?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| gap_condescension | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 6. dev-programmatic-001-ai-maturity-structured-reply

- failure_dimension: `ai_maturity_consistency`
- difficulty: `hard`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `ai_maturity_consistency, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Re: workflow signal review
Body: Hi Felix, The visible CRM workflow still points to an intermediate automation state rather than a broad capability claim. Can you reply with one stalled handoff so we can keep the workflow diagnosis grounded?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| ai_maturity_consistency | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 7. dev-programmatic-004-ai-maturity-structured-reply

- failure_dimension: `ai_maturity_consistency`
- difficulty: `hard`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `ai_maturity_consistency, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Body: Hi Rafael, The visible CRM workflow still points to an intermediate automation state rather than a broad capability claim. Can you reply with one stalled handoff so we can keep the workflow diagnosis grounded?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| ai_maturity_consistency | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 8. dev-trace-derived-007-ai-maturity-structured-visibility

- failure_dimension: `ai_maturity_consistency`
- difficulty: `hard`
- source_mode: `trace_derived`
- partition: `dev`
- judge_dimensions: `ai_maturity_consistency, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Re: maturity signal review
Body: Hi Camila, The CRM instrumentation and workflow ownership signals should stay explicit instead of collapsing into generic prose. Can you reply with one example where the workflow handoff stalls so the maturity read stays grounded?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| ai_maturity_consistency | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 9. dev-trace-derived-010-ai-maturity-structured-visibility

- failure_dimension: `ai_maturity_consistency`
- difficulty: `hard`
- source_mode: `trace_derived`
- partition: `dev`
- judge_dimensions: `ai_maturity_consistency, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Re: maturity signal review
Body: Hi Leah, The CRM instrumentation and workflow ownership signals should stay explicit instead of collapsing into generic prose. Can you reply with one example where the workflow handoff stalls so the maturity read stays grounded?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| ai_maturity_consistency | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 10. dev-programmatic-037-maturity-score-conservative

- failure_dimension: `ai_maturity_consistency`
- difficulty: `easy`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `ai_maturity_consistency, signal_grounding, output_validity`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Question on maturity read
Body: Hi Camila, The maturity signal here stays at score 1 with low confidence, so the workflow framing should stay exploratory rather than assertive. Can you share one workflow example that would help validate the maturity read?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| ai_maturity_consistency | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| output_validity | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 11. dev-programmatic-021-output-clean-abstain

- failure_dimension: `output_validity`
- difficulty: `easy`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `output_validity, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Question on queue pressure
Body: Hi Rina, The visible workflow evidence is still too weak for a strong claim, so the draft should stay precise instead of generic. Can you reply with one queue example if the outside workflow signal is incomplete?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| output_validity | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 12. dev-programmatic-024-output-clean-abstain

- failure_dimension: `output_validity`
- difficulty: `easy`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `output_validity, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Body: Hi Tom, The visible workflow evidence is still too weak for a strong claim, so the draft should stay precise instead of generic. Can you reply with one queue example if the outside workflow signal is incomplete?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| output_validity | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 13. dev-trace-derived-019-thin-evidence-restraint

- failure_dimension: `output_validity`
- difficulty: `easy`
- source_mode: `trace_derived`
- partition: `dev`
- judge_dimensions: `output_validity, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Question on workflow load
Body: Hi Noor, A small number of public signals are visible, but they still do not prove a real workflow queue problem. Can you reply with one queue example if the outside workflow signal is missing something material?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| output_validity | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 14. dev-trace-derived-022-thin-evidence-restraint

- failure_dimension: `output_validity`
- difficulty: `easy`
- source_mode: `trace_derived`
- partition: `dev`
- judge_dimensions: `output_validity, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Body: Hi Felix, A small number of public signals are visible, but they still do not prove a real workflow queue problem. Can you reply with one queue example if the outside workflow signal is missing something material?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| output_validity | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 15. dev-programmatic-041-reengagement-format-check

- failure_dimension: `output_validity`
- difficulty: `medium`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `output_validity, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Re: workflow follow-up
Body: Hi Felix, A well-formed reengagement should stay specific about the workflow bottleneck rather than drift into generic prose. Can you send one queue example if the outside signal is missing something material?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| output_validity | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 16. dev-programmatic-005-thin-signal-restraint

- failure_dimension: `signal_grounding`
- difficulty: `easy`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `signal_grounding, style_guide_adherence, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Question on workflow load
Body: Hi Rafael, A few public hiring signals are visible, but they are still too thin to claim a real workflow queue issue. Can you share one place where the workflow queue actually slows down if the outside signal is missing something?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 17. dev-programmatic-008-thin-signal-restraint

- failure_dimension: `signal_grounding`
- difficulty: `easy`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `signal_grounding, style_guide_adherence, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Body: Hi Jess, A few public hiring signals are visible, but they are still too thin to claim a real workflow queue issue. Can you share one place where the workflow queue actually slows down if the outside signal is missing something?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 18. dev-programmatic-025-pricing-scope-boundary

- failure_dimension: `signal_grounding`
- difficulty: `hard`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `signal_grounding, style_guide_adherence, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Question on pricing scope
Body: Hi Tom, The workflow signal here only supports a public_bands_only pricing scope, so any route-specific rate conversation needs a human reviewer first. Can you reply with one pricing question that still fits within the public scope?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 19. dev-programmatic-027-pricing-scope-boundary

- failure_dimension: `signal_grounding`
- difficulty: `hard`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `signal_grounding, style_guide_adherence, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Body: Hi Felix, Keeping the pricing scope explicit means the conversation stays grounded in what the public signal can actually support. Can you send one example where the scope needs to be confirmed before any rate discussion?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 20. dev-programmatic-028-pricing-scope-boundary

- failure_dimension: `signal_grounding`
- difficulty: `hard`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `signal_grounding, style_guide_adherence, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Question on pricing scope
Body: Hi Dana, The workflow signal here only supports a public_bands_only pricing scope, so any route-specific rate conversation needs a human reviewer first. Can you reply with one pricing question that still fits within the public scope?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 21. dev-programmatic-009-fixture-live-boundary

- failure_dimension: `style_guide_adherence`
- difficulty: `medium`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `style_guide_adherence, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Re: artifact provenance
Body: Hi Jess, The artifact in question came from a fixture-backed review path rather than a live production run. Can you reply if you want the production-safe review criteria we use before external sharing?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 22. dev-programmatic-012-fixture-live-boundary

- failure_dimension: `style_guide_adherence`
- difficulty: `medium`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `style_guide_adherence, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Body: Hi Kevin, The artifact in question came from a fixture-backed review path rather than a live production run. Can you reply if you want the production-safe review criteria we use before external sharing?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 23. dev-trace-derived-013-demo-boundary-honesty

- failure_dimension: `style_guide_adherence`
- difficulty: `medium`
- source_mode: `trace_derived`
- partition: `dev`
- judge_dimensions: `style_guide_adherence, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Re: artifact provenance
Body: Hi Omar, The artifact came from a fixture-backed review path rather than a live production run. Can you reply if the production-safe review checklist would be more useful than another artifact?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 24. dev-trace-derived-016-demo-boundary-honesty

- failure_dimension: `style_guide_adherence`
- difficulty: `medium`
- source_mode: `trace_derived`
- partition: `dev`
- judge_dimensions: `style_guide_adherence, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Body: Hi Rina, The artifact came from a fixture-backed review path rather than a live production run. Can you reply if the production-safe review checklist would be more useful than another artifact?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 25. dev-programmatic-045-style-prefix-explicit

- failure_dimension: `style_guide_adherence`
- difficulty: `easy`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `style_guide_adherence, signal_grounding, next_step_quality`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Re: review scope note
Body: Hi Rafael, The review scope should stay explicit so the buyer knows which artifacts are fixture-backed before the conversation advances. Can you reply with one review question that still needs a scope clarification?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 26. dev-programmatic-017-timezone-aware-next-step

- failure_dimension: `next_step_quality`
- difficulty: `medium`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `next_step_quality, signal_grounding, style_guide_adherence`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Re: local-time availability
Body: Hi Mina, The outreach is more credible when the local time window is treated as a buyer constraint rather than an afterthought. Can you share one local meeting window that works so we stay inside business hours?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 27. dev-programmatic-020-timezone-aware-next-step

- failure_dimension: `next_step_quality`
- difficulty: `medium`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `next_step_quality, signal_grounding, style_guide_adherence`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Body: Hi Rina, The outreach is more credible when the local time window is treated as a buyer constraint rather than an afterthought. Can you share one local meeting window that works so we stay inside business hours?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 28. dev-programmatic-029-capacity-gate-first

- failure_dimension: `next_step_quality`
- difficulty: `hard`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `next_step_quality, signal_grounding, style_guide_adherence`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Question on capacity gate
Body: Hi Dana, The capacity gate has to stay open before any delivery commitment can be confirmed. Can you share the one capacity question that still needs to clear before we discuss delivery?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 29. dev-programmatic-030-capacity-gate-first

- failure_dimension: `next_step_quality`
- difficulty: `hard`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `next_step_quality, signal_grounding, style_guide_adherence`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Re: Note on delivery gate
Body: Hi Mina, Skipping the capacity gate means any next-step commitment would be premature given the current capacity state. Can you reply with the gate criteria that would let us move to a timeline conversation?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

### 30. dev-programmatic-032-capacity-gate-first

- failure_dimension: `next_step_quality`
- difficulty: `hard`
- source_mode: `programmatic`
- partition: `dev`
- judge_dimensions: `next_step_quality, signal_grounding, style_guide_adherence`
- deterministic baseline: `PASS` via `src/scoring/scoring_evaluator.py`

```text
Subject: Question on capacity gate
Body: Hi Noor, The capacity gate has to stay open before any delivery commitment can be confirmed. Can you share the one capacity question that still needs to clear before we discuss delivery?
```

| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |
|---|---|---|---|---|---|---|
| next_step_quality | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| signal_grounding | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |
| style_guide_adherence | n/a | pass | pass | pass | agree | second_pass_2026-05-02; second_labeler_2026-05-02 |

## Per-Dimension Agreement Matrix

Each dimension is reviewed across the 30 tasks where that dimension is in the task's
`judge_dimensions`. Raw agreement is the share of rows where two labels match. Cohen's kappa is
reported alongside raw agreement; with all labels at `pass` after revision, kappa is undefined
(zero variance) and reported as `n/a`, which the methodology treats as a pass when raw agreement
is 100%.

### Test-Retest (labeler A, 48h gap, blind to first pass)

| rubric_dimension | tasks | raw_agreement | cohen_kappa | wilson_95_ci | status |
|---|---:|---:|---:|---|---|
| `gap_condescension` | 30 | 1.00 (30/30) | n/a | [0.886, 1.000] | pass |
| `ai_maturity_consistency` | 30 | 1.00 (30/30) | n/a | [0.886, 1.000] | pass |
| `output_validity` | 15 | 1.00 (15/15) | n/a | [0.796, 1.000] | pass |
| `signal_grounding` | 30 | 1.00 (30/30) | n/a | [0.886, 1.000] | pass |
| `style_guide_adherence` | 30 | 1.00 (30/30) | n/a | [0.886, 1.000] | pass |
| `next_step_quality` | 30 | 1.00 (30/30) | n/a | [0.886, 1.000] | pass |

### Inter-Rater (labeler A vs labeler B, independent)

| rubric_dimension | tasks | raw_agreement | cohen_kappa | wilson_95_ci | status |
|---|---:|---:|---:|---|---|
| `gap_condescension` | 30 | 1.00 (30/30) | n/a | [0.886, 1.000] | pass |
| `ai_maturity_consistency` | 30 | 1.00 (30/30) | n/a | [0.886, 1.000] | pass |
| `output_validity` | 15 | 1.00 (15/15) | n/a | [0.796, 1.000] | pass |
| `signal_grounding` | 30 | 1.00 (30/30) | n/a | [0.886, 1.000] | pass |
| `style_guide_adherence` | 30 | 1.00 (30/30) | n/a | [0.886, 1.000] | pass |
| `next_step_quality` | 30 | 1.00 (30/30) | n/a | [0.886, 1.000] | pass |

### Final Agreement Summary (Post-Revision)

All six rubric dimensions pass the 80% raw-agreement threshold on both test-retest and inter-rater
passes. The `ai_maturity_consistency` dimension is the one revised dimension, and it passes after
the rubric tightening described in the changelog above. The held-out partition can therefore be
treated as human-calibrated for sealing purposes.

## Reporting Notes

- The 30-task subset, the rubric revision changelog, and both agreement passes are reproducible
  from `docs/inter_rater_subset.jsonl` and the per-task tables in this file.
- Do not overwrite existing human labels when refreshing the subset or rerendering this template.
- The deterministic baseline column is a scaffold; the agreement numbers above are derived strictly
  from the human-entered `first_pass_label`, `second_pass_label`, and `second_labeler_label`
  columns.
