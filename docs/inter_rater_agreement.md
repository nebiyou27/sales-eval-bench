# Inter-Rater Agreement - Tenacious-Bench v0.1

Generated: 2026-04-30. This workflow is prepared, but final human agreement remains pending until
the label columns below are filled by one human on first pass, the same human on second pass after
at least 24 hours, and ideally a second human labeler.

Subset path: `docs/inter_rater_subset.jsonl`

Status note: the deterministic baseline below is preserved for reference only. It is not human
agreement and should not be reported as human calibration.

## Protocol Status

- Subset prepared: 30 dev-only tasks, stratified to 5 tasks per failure dimension.
- Human first-pass labels: pending.
- Human second-pass labels: pending. Scheduled relabel time: 2026-05-01.
- Second labeler review: pending.
- Agreement calculator: `python src/scoring/compute_inter_rater_agreement.py`.

## Human Label Scale

Use a simple label per rubric dimension such as `pass`, `fail`, `unsure` or a consistent `1-5`
rating scale. Keep one scale throughout a pass.

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
| gap_condescension | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| gap_condescension | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| gap_condescension | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| gap_condescension | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| gap_condescension | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| ai_maturity_consistency | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| ai_maturity_consistency | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| ai_maturity_consistency | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| ai_maturity_consistency | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| ai_maturity_consistency | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| output_validity | n/a |  |  |  |  |  |

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
| output_validity | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| output_validity | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| output_validity | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| output_validity | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| output_validity | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| signal_grounding | n/a |  |  |  |  |  |
| style_guide_adherence | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| signal_grounding | n/a |  |  |  |  |  |
| style_guide_adherence | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| signal_grounding | n/a |  |  |  |  |  |
| style_guide_adherence | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| signal_grounding | n/a |  |  |  |  |  |
| style_guide_adherence | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| signal_grounding | n/a |  |  |  |  |  |
| style_guide_adherence | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| style_guide_adherence | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| style_guide_adherence | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| style_guide_adherence | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| style_guide_adherence | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| style_guide_adherence | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| next_step_quality | n/a |  |  |  |  |  |

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
| next_step_quality | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| style_guide_adherence | n/a |  |  |  |  |  |

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
| next_step_quality | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| style_guide_adherence | n/a |  |  |  |  |  |

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
| next_step_quality | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| style_guide_adherence | n/a |  |  |  |  |  |

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
| next_step_quality | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| style_guide_adherence | n/a |  |  |  |  |  |

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
| next_step_quality | n/a |  |  |  |  |  |
| signal_grounding | n/a |  |  |  |  |  |
| style_guide_adherence | n/a |  |  |  |  |  |

## Reporting Notes

- If the human label fields are still blank, report the protocol as prepared but incomplete.
- Do not overwrite existing human labels when refreshing the subset or rerendering this template.
- Treat the deterministic baseline as a scaffold only; the actual agreement numbers must come from
  human-entered labels in `docs/inter_rater_subset.jsonl`.
