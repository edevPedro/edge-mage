# Conceito — Quantização: pesos em baixa precisão

Modelos treinam em fp32/fp16, mas para *servir* não precisam de toda a
precisão. **Quantização** mapeia pesos (e ativações) para int8/int4, cortando
memória, acelerando acesso ao cache e reduzindo energia — trocando um pouco de
precisão por um orçamento 4× (ou 8×) menor.

## 1. Quantização simétrica (int8)
```
scale = max(|min_val|, |max_val|) / 127
q(w)  = round(w / scale)         (clamped em [-127, 127])
w'    = q(w) * scale             (reconstrução)
erro  = |w - w'|
```
- Ponto fixo: ao escurecer o intervalo de pesos num `scale` único, o range
  inteiro cabe em 8 bits.
- **Outliers** (ex.: ativações grandes em algumas dimensões de transformers
  fp16→int8) esticam o scale e "esmagam" o resto — problema clássico resolvido
  por técnicas como *mixed-precision decomposition* (LLM.int8).

## 2. PTQ vs QAT
- **PTQ (post-training quantization)**: quantiza après o treino, com uma
  calibração (algumas batches). Rápido, mas pode degradar mais.
- **QAT (quantization-aware training)**: simula a quantização *durante* o
  treino (forward-quantizado, gradiente passa through). Melhor qualidade, mais
  caro.
- Em BCI edge (EEGNet, poucos parâmetros) o PTQ costuma bastar; a perda de
  qualidade deve ser medida com a mesma validação rigorosa do treino.

## 3. Ganhos em inference engineering
- **Memória**: fp32→int8 = 4× menor de pesos; dobra para o KV cache
  (ver `nt-kv-cache`).
- **Latência**: pesos menores cabem mais em cache (bandwidth-bound decode);
  em hardware com núcleos int8 (comum em NPU/edge), o matmul int8 é mais rápido.
- **Formato**: `nt-model-formats` decide quantos bits usar por camada.

## O que a próxima sala assume
`nt-inf-metrics` mede o que essa troca fez: latência, vazão e percentis antes e
depois de quantizar — sem medição, a otimização é cosmética.

## Leituras recomendadas
- [PyTorch — quantization (PTQ/QAT)](https://pytorch.org/docs/stable/quantization.html)
- [LLM.int8() — Dettmers et al.](https://arxiv.org/abs/2208.07339)
- [llama.cpp GGUF formats](https://github.com/ggml-org/llama.cpp)