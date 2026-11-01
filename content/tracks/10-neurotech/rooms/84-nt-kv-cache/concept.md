# Conceito — KV Cache: a memória que cresce com a conversa

Durante o prefill, a atenção calcula as chaves (K) e valores (V) de todos os
tokens do contexto. Sem reutilizá-los, cada token novo do decode recomputaria a
atenção do contexto inteiro — um desperdício O(L) por passo. O **KV cache**
guarda K/V para o decode só calcular atenção do *novo* token contra o passado.

## 1. O que é armazenado
- Por camada do modelo, por cabeça: `K` e `V` de cada token processado.
- Tamanho total (memória do working set):
```
bytes = seq_len × n_layers × n_heads × head_dim × 2 × dtype_bytes
                          (K e V)
```
- Exemplo realista: 2.048 tokens, 32 camadas, 32 cabeças, 128 dim, fp16 →
  ≈ 2,14 GB **só de cache** — na prática maior que os pesos de muitos modelos.

## 2. Por que ele domina
- Pesos são fixos (podem ficar em flash/uma cópia). O cache **cresce a cada
  token** — conversas longas, batch grande e contexto grande estouram RAM/VRAM.
- É este o gargalo do decode (memory-bound), e onde fica a fragmentação:
  cada requisição aloca blocos contíguos desiguais.

## 3. PagedAttention (vLLM)
- Analogia com memória virtual: o cache é partido em **blocos paginados**,
  alocados sob demanda, não contíguos. Elimina fragmentação e permite
  *sharing* de prefixos comuns entre requisições (prefix caching).

## 4. Compressão
- Cache KV por cabeça: existem compressões (técnicas como 4-bit KV, eviction
  de tokens menos importantes) — sempre há o trade-off qualidade × memória.

## O que a próxima sala assume
`nt-quantization` reduz pesos (e depois cache) com inteiros de baixa precisão —
a técnica que mais corta bytes no modelo *e* trava o crescimento do cache.

## Leituras recomendadas
- [Transformer Inference Arithmetic (Kipply)](https://kipp.ly/transformer-inference-arithmetic/) — a matemática do cache.
- [PagedAttention (Kwon et al.)](https://arxiv.org/abs/2309.06180)
- [vLLM — design docs](https://docs.vllm.ai/en/latest/design.html)