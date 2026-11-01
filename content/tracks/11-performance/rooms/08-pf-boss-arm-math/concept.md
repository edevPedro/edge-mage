# Conceito — Performance Boss (padrão)

Todo boss Performance segue o ritual:

1. **Duas implementações** (baseline clara + otimizada).
2. **Medir** no mesmo harness (tempo ± contadores).
3. **Explicar** o ganho (Roofline / misses / vetorização).
4. **Provar correção** contra golden (tolerância explícita).

## Projeto — ARM Math Library (stub)

Entregue um mini-lib: `dot`, `saxpy`, `relu` ou `mean` — scalar + NEON/autovec — com README de evidência em `study-log/artifacts/perf-arm-math.md`.

