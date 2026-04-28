# Cost Controls

## Budget

Total cap: USD 10.

| Bucket | Cap | Rule |
|---|---:|---|
| Dataset authoring | USD 3-5 | Use dev-tier OpenRouter calls only for task synthesis, dedup, and judge filtering. |
| Training | USD 0-5 | Prefer free Colab T4. Use RunPod only if Colab caps block the scheduled smoke test. |
| Held-out evaluation | USD 2-3 | Run only after the benchmark split is sealed. |
| Reserve | USD 1-2 | Use only with a note in `cost/log.csv`. |

## Hard Rules

- No tau2-Bench retail reruns this week.
- No eval-tier authoring or dedup calls on Days 2-3.
- Log every smoke test, synthesis call, judge call, training run, and held-out pass in `cost/log.csv`.
- Every log row must include timestamp, bucket, provider, model or compute target, purpose, estimated cost, actual cost, and notes.
