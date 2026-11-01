# Conceito — Medir de verdade

Performance Boss exige **evidência**: tempo wall + (quando possível) contadores / Instruments.

## Armadilhas

- Comparar M4 com Cortex-A sem normalizar.
- Benchmark sem warm-up / com power throttling.
- Otimizar o harness errado.

## Ritual mínimo

1. Fixar input e seed.
2. Rodar N≥30 (ou critério estável).
3. Reportar mediana + p95.
4. Anotar máquina (chip, OS, flags).

