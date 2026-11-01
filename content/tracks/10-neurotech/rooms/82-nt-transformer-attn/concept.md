# Conceito — Transformer e mecanismo de atenção

O bloco do transformer troca o deslizar de janelas fixas (RNN/CNN) por uma
operação em que **todo token pode olhar todo token**: a *attention*. É o
coração dos LLMs e o motivo de a inferência ter um formato prefill/decode.

## 1. Query, Key, Value
- Cada token projeta sua representação em três vetores (via matrizes treináveis):
  - **Query (Q)**: *o que estou procurando*;
  - **Key (K)**: *o que eu ofereço/descrevo*;
  - **Value (V)**: *o conteúdo que realmente carrego*.
- Pontuação de parede entre token `i` e token `j`:
  `score = Q_i · K_j` (produto escalar, com escala `1/sqrt(d_k)`).

## 2. Cálculo da atenção
```
S = (Q @ Kᵀ) * scale        # L×L pesos de pareamento
P = softmax_row(S)          # normaliza por linha (pesos >= 0, soma 1)
A = P @ V                    # cada saída mistura os V conforme os pesos
```
- `softmax_rows`: cada linha soma 1 — os "quanto o token i atende cada outro".
- Escala `1/sqrt(d_k)`: sem ela, logits grandes saturariam o softmax
  (gradientes ~0).

## 3. Por que custo O(L²) importa
- Para `L` tokens de contexto, `Q@Kᵀ` é `L×L` → memória e tempo **quadráticos**.
- É a fonte do *kv-cache working set* (`nt-kv-cache`) e, em janelas longas
  (ex.: long context), a primeira coisa que estoura orçamento de RAM/latência.

## 4. Transformer block (resumo)
1. Multi-head self-attention (várias cabeças paralelas = diferentes tipos de
   relação);
2. FFN por token; residuals (`x + attn(x)`) e LayerNorm estabilizam o treino.

## O que a próxima sala assume
`nt-llm-generate` usa a atenção para *gerar*: prefill do contexto e decode
token a token — e as métricas de latência dessa operação.

## Leituras recomendadas
- [Attention is All You Need](https://arxiv.org/abs/1706.03762)
- [The Illustrated Transformer (Alammar)](https://jalammar.github.io/illustrated-transformer/)
- [Karpathy — Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY)