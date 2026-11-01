# Ritual template — Performance Boss

Copy into `study-log/artifacts/<name>.md` for each boss.

## Metadata

- Room id:
- Machine (chip / OS / RAM):
- Compiler / flags / SDK:
- Date:

## 1. Two implementations

| Version | Path / entry | Notes |
|---------|--------------|-------|
| Baseline | | Clarity over speed |
| Optimized | | SIMD / tile / Metal / RTL |

## 2. Measurement

| Metric | Baseline | Optimized | N runs | Notes |
|--------|----------|-----------|--------|-------|
| Wall time (median) | | | | |
| p95 | | | | |
| Counters / Instruments (optional) | | | | |

Protocol: fixed input, warm-up policy stated, no silent DVFS surprises if avoidable.

## 3. Explanation

- Arithmetic intensity estimate (flops/byte):
- Bound (memory / compute / other):
- Why the optimized version won (or did not):

## 4. Numerical correctness

- Golden source:
- Tolerance (abs / rel):
- Max error observed:
- Pass? (yes/no):

## M4 / platform notes

- [ ] Documented that µarch ≠ Cortex-A if comparing Arm mobile docs
- [ ] Did not claim SVE on Apple Silicon M4
- [ ] Metal≠CUDA acknowledged if GPU involved
