# Day 1 Seed Inventory

## Artifact Status

| Artifact | Status | Notes |
|---|---|---|
| `seed/trace_log.jsonl` | present, parseable | 150 JSONL records; 109 reward=1.0, 41 reward=0.0 |
| `seed/held_out_traces.jsonl` | present, parseable | 17 JSONL records; 9 reward=1.0, 8 reward=0.0 |
| `seed/probe_library.md` | present, readable | Probe IDs P01-P35 and Tenacious reframes T01-T06 found |
| `seed/failure_taxonomy.md` | present, readable | Measured categories include AI maturity validity and gap condescension |

## Probe IDs For Audit Memo

| Probe | Failure mode | Why diagnostic | Benchmark dimension |
|---|---|---|---|
| P05 | Tier mood | Catches overconfident claims from weak evidence | signal_grounding |
| P24 | AI maturity lossiness | Captures invalid or prose-only AI maturity outputs | ai_maturity_consistency |
| P26 | Invented AI maturity source URL | Tests unsupported public-signal attribution | signal_grounding |
| P27 | Gap over-claiming | Prevents fabricated competitor-gap outreach | gap_condescension |
| P29 | Thin evidence | Forces abstention when no actionable claims exist | output_validity |
| P30 | Fixture/live boundary | Prevents demo artifacts from being presented as production | style_guide_adherence |
| P33 | Gap condescension | Targets intrusive capability-gap language for sophisticated buyers | gap_condescension |
| P35 | Multi-thread leakage | Checks account-level consistency across contacts | ai_maturity_consistency |

## Trace Examples For Audit Memo

| Trace ID | Task ID | Source | Reward | Failure mode | Why diagnostic |
|---|---|---|---|---|---|
| a553180f-80d2-4d4b-9a1e-d525b1219cfd | 11 | trace_log | 0.0 | failed retail trace | Candidate rejected example for benchmark contrast |
| 89337dd1-bb36-41d7-8530-190df8734cc3 | 34 | trace_log | 0.0 | failed retail trace | Candidate rejected example for benchmark contrast |
| ef2ad255-479a-4b67-a96f-2522026e3aaf | 66 | trace_log | 0.0 | failed retail trace | Candidate rejected example for benchmark contrast |
| 0857ba6e-d8cb-4ec8-b024-3d5ddc298fc6 | 76 | trace_log | 0.0 | failed retail trace | Candidate rejected example for benchmark contrast |
| 19d13ac9-f495-4df4-b1c4-d042ca754933 | 92 | trace_log | 0.0 | failed retail trace | Candidate rejected example for benchmark contrast |

## Starter Preference Candidates

Use reward=1.0 traces as provisional chosen examples and reward=0.0 traces as provisional rejected examples. These are flags for Day 1 inspection, not final ORPO pairs.

| Role | Trace ID | Task ID | Source | Reward |
|---|---|---|---|---|
| rejected | a553180f-80d2-4d4b-9a1e-d525b1219cfd | 11 | trace_log | 0.0 |
| rejected | 89337dd1-bb36-41d7-8530-190df8734cc3 | 34 | trace_log | 0.0 |
| rejected | ef2ad255-479a-4b67-a96f-2522026e3aaf | 66 | trace_log | 0.0 |
| chosen | 9f1bceea-557f-4086-b5f0-ddebed571544 | 1 | trace_log | 1.0 |
| chosen | 3bb05cae-be14-405a-866c-7355eccde196 | 2 | trace_log | 1.0 |
| chosen | 85051d0d-3245-4ddb-b366-2ecb00df4ece | 7 | trace_log | 1.0 |
