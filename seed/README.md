# Seed Inputs (Read-Only)

Week 10 Conversion Engine evidence. Treat these files as immutable provenance for the Week 11
benchmark — code in `src/` reads from here but never writes back.

| File | Purpose |
|---|---|
| `trace_log.jsonl` | Week 10 task-level reward, timing, and identifiers used to derive trace-derived tasks and ORPO rejected examples. |
| `held_out_traces.jsonl` | Trace IDs that must never appear in `train` or `dev`; enforced by `assert_no_held_out_leakage`. |
| `probe_library.md` | Probe IDs (P05, P24, P27, P29, P30, P33, …) and their measured incident rates. Cited by `audit_memo.md` and `methodology.md`. |
| `failure_taxonomy.md` | Week 10 failure-mode definitions and observed incidence rates. |

Adding new seed evidence: drop a new file here and reference it from the relevant doc; do not
mutate the existing files.
