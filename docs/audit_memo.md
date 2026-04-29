# Audit Memo

Tenacious-Bench cannot be replaced by a generic public retail benchmark because the highest-cost
failures in Week 10 were not generic sales-writing mistakes. They were Tenacious-specific trust
failures: weak public signals turned into overconfident claims, sophisticated buyers addressed as if
they lacked basic AI maturity, fixture/live-boundary mistakes where demo artifacts were treated as
production evidence, and account context handled inconsistently across contacts. Public retail
benchmarks may score fluency, but they do not stress buyer-respect, signal entitlement, or
account-level consistency.

The required missing dimensions are already visible in the Week 10 probe set. P05 tests tier-mood
control when the evidence is weak. P24 tests whether AI-maturity output remains structured and
usable instead of collapsing into empty or invalid JSON. P26 tests invented AI-maturity source URLs.
P27 tests abstention when no peer-evidence exists for a competitor-gap claim. P29 tests thin-evidence
restraint. P30 tests fixture/live boundary honesty. P33 tests gap-condescension toward sophisticated
buyers. P35 tests multi-thread leakage across contacts at the same account. Together, these probes
describe benchmark requirements that a generic retail task suite does not cover.

The Week 10 artifacts show these are not hypothetical concerns. `seed/trace_log.jsonl` already
contains at least five reward-0.0 examples queued for audit evidence:
`a553180f-80d2-4d4b-9a1e-d525b1219cfd` / task 11 is the concrete rejected example for
competitor-gap condescension, `89337dd1-bb36-41d7-8530-190df8734cc3` / task 34 is the rejected
example for AI-maturity consistency loss, `ef2ad255-479a-4b67-a96f-2522026e3aaf` / task 66 is a
rejected unsupported-evidence example, `0857ba6e-d8cb-4ec8-b024-3d5ddc298fc6` / task 76 is the
fixture/live-boundary honesty example, and `19d13ac9-f495-4df4-b1c4-d042ca754933` / task 92 is the
thin-evidence restraint example. These traces matter because they provide concrete failed agent
behaviors that can be converted into Tenacious-Bench tasks and chosen/rejected preference pairs.
Their detailed preference use remains tracked in the Day 1 evidence inventory.

The measured rates in `seed/failure_taxonomy.md` make the main gap even clearer. P24 produced the
highest observed incident rate: 43.3% on tau2 thinking-model runs, where hard AI-maturity tasks
returned empty or invalid JSON. P33 produced the highest business-risk rate: 15.6% on A/B
signal-grounded outreach, where competitor-gap language became intrusive or presumptuous.
`seed/probe_library.md` also shows that P05 contributes a 6.3% tier-mood problem, while P30, P27,
and P29 define the abstention and honesty boundaries that kept deterministic parts of the Week 10
system safer.

The core issue, then, is not only generation quality. The bigger issue is self-detection of bad
outputs. The system can often produce plausible text, yet still fail to detect when the output is
unsupported, invalid, condescending, or inconsistent with buyer context. That is why Act I should
center on a benchmark rubric that makes those failures machine-checkable first, then judge-checkable
where needed.

Recommendation: continue with Path B, a preference-tuned judge / critic. The Week 10 evidence
shows the agent does not only need better generation; it needs a reliable rejection layer that can
rank grounded, buyer-respectful, structurally valid outputs above unsafe, unsupported, or
presumptuous alternatives. Tenacious-Bench should therefore evaluate not just whether the agent can
produce an answer, but whether it can identify when an answer should be accepted, revised, or
blocked.
