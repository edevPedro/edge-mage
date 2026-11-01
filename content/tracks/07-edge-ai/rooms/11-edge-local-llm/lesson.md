# LLM local no edge

LLMs pequenos (GGUF / TinyLlama / SmolLM) são viáveis em MCU, mas o board que roda ganham apenas se o **orçamento de RAM** fechar:

```
RAM ≤ pesos · MODEL_MB + cache_KV + arena de ativações
```

## Cache KV

Cada token novo precisa de K e V para as camadas de atenção:

```
KV/token = 2 · n_layers · n_kv_heads · head_dim · dtype_bytes
```

Em int8 (dtype 1 B), com 6 layers, 2 KV-heads e head_dim 64: **1536 B/token**. Com 512 tokens de contexto ≈ 0,8 MB — isso é decisivo num MCU de 256 KB! Por isso a quantização de cache KV [é tema quente](https://arxiv.org/abs/2407.09056) — e por isso o EdgeBERT comprime o modelo todo.

## Pontos de inflexão

- **Context floats vs contexto trivial**: 2× em `seq_len`, `n_kv_heads`, `head_dim` — cada ponto dobra RAM de contexto.
- **Quantização do cache**: int8KV corta o KV pela metade (1536 → 768 B/token contando scale).
- **Pesos em 4–8 bits** (GGUF `q8_0`, `q4_0`): o `.gguf` no disco não é a conta da RAM; a conta é o modelo _descomprimido_ na memória.

`context_fits` da sala é o check gate: `modelo + n_len·KV ≤ RAM` — se não fecha, reduz contexto ou quantiza mais.