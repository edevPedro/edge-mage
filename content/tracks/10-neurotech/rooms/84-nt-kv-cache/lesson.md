# Desafio — KV cache: append, scores e a conta de memória

## 1. Objetivo do Desafio
Implementar o contrato do KV cache (append de K/V do novo token) e a fórmula
que governa o working set de atenção: `bytes = seq_len × n_layers × n_heads ×
head_dim × 2 (K e V) × dtype_bytes`.

## 2. Especificação Técnica e Formulação
- `kv_cache_append(cache, K, V)` → `[cache[0] + K, cache[1] + V]` (convolve
  listas; `cache = [[...K acumuladas], [...V acumuladas]]`).
- `cached_scores(Q_last, K_cache, scale)` → lista `[scale · ∑_d Q_last[d]·K[d]]
  over each key in K_cache`.
- `kv_cache_bytes(seq_len, n_layers, n_heads, head_dim, dtype_bytes=2)`.

## 3. Critérios de Validação e Armadilhas
- O `2` final da fórmula é K e V; o `dtype_bytes` padrão é 2 (fp16/bfloat16).
- `cached_scores` usa a *última query* contra *todas as keys* (1×L).
- Decore os 2.048/32/32/128 → ≈2 GB como referência de trabalho.