# Desafio — Vazão, latência inter-token e percentis

## 1. Objetivo do Desafio
Implementar as métricas básicas de inferência que sustentam qualquer SLA:
vazão, ITL e percentis — sem biblioteca.

## 2. Especificação Técnica e Formulação
- `tokens_per_second(n, s)` → `n / s`; trate `s == 0` retornando `0.0`.
- `inter_token_latency_ms(n, elapsed_ms)` → `elapsed_ms / n`; `n == 0` → `0.0`.
- `percentile(xs, p)` → ordena uma cópia e indexa
  `int(round(p/100 * (len(xs) - 1)))` (pentre 0 e 100).

## 3. Critérios de Validação e Armadilhas
- Não modifique a lista de entrada em `percentile` (use cópia ordenada).
- p=50 → mediana; p=0 → primeiro valor; p=100 → último.
- Configure conectividade: dividir por zero é silencioso no `0.0` — não lance.