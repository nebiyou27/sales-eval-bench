# Tests

Test files mirror the `src/` layout: `test_<module>.py` per module under test.

```bash
pytest tests/
```

Tests run against the committed `train/` and `dev/` partitions plus the smoke fixtures under
`tenacious_bench_v0.1/smoke/`. They never touch `held_out/`.
