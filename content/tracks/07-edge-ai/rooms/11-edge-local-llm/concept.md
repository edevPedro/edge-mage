# Conceito — LLM local no edge

## Orçamento de RAM
`pesos + cache KV + arena ≤ RAM disponível`.

## Cache KV
`KV/token = 2 · n_layers · n_kv_heads · head_dim · dtype_bytes`. Em int8KV, 1536 B/token (6L·2H·64d).

## Contexto
`n_len · KV/token + modelo ≤ RAM` decide se o contexto cabe.