# Conceito — Portal Deep Learning & Inference Engineering

Este módulo (**F15-dl-inf**) amplia o pilar F8-decode: você já domina a baseline
(CSP + LDA), a arquitetura compacta EEGNet e os orçamentos de latência do loop
online. Agora o objetivo é dominar o vocabulário de quem *serve* e *otimiza*
modelos na prática — de redes profundas em dados neurais até o pipeline de
inferência em produção, usando como mapa o roadmap.sh/inference-engineering.

## 1. Por que Deep Learning (e quando não usar)

- **N ≫ D**: com muitos exemplos, arquiteturas profundas generalizam (visão,
  linguagem — bilhões de amostras).
- **N ≪ D**: em neuro/BCI, o regime típico é centenas de trials × dezenas de
  milhares de dimensões. Deep só ajuda com *inductive bias* forte (convoluções
  temporais = filter-bank, espaciais depthwise = CSP) e regularização agressiva.
- Decisão de engenharia: comece pela baseline linear; suba para deep quando a
  baseline saturar e houver pipeline de validação confiável (inter-session,
  cross-subject).

## 2. O mapa da inferência (roadmap.sh)

| Área | O que ensina | Onde no círculo |
|------|--------------|-----------------|
| Neural / Transformers | MLP, CNN, attention, KV cache, embedding | `nt-ml-mlp` → `nt-transformer-attn` |
| Geração LLM | prefill/decode, TTFT, ITL, tokens/s | `nt-llm-generate` |
| Otimização | quantização, attention-opt, caching | `nt-quantization`, `nt-kv-cache` |
| Serviço | batching contínuo, engines, formatos | `nt-model-formats`, `nt-serving-batching` |
| Medição | latência/throughput/percentis, roofline | `nt-inf-metrics` |

## 3. Vocabulário mínimo antes dos labs

- **Inferência ≠ treino**: forward fixo com pesos congelados; métricas de
  latência, não de loss.
- **TTFT / ITL / tokens·s⁻¹ / RTF**: tempo do primeiro token, tempo entre
  tokens, vazão e real-time factor.
- **Prefill vs decode**: processar o contexto de uma vez (paralelo) vs gerar
  token a token (sequencial) — a mesma tensão *janela vs latência* do loop
  online BCI.

## O que a próxima sala assume

`nt-ml-mlp` assume MLP one-hidden-layer: forward com ReLU, contagem de
parâmetros e por que profundidade ≠ largura.

## Leituras recomendadas

- [Roadmap.sh — Inference Engineering](https://roadmap.sh/inference-engineering)
  — o mapa que estrutura este módulo inteiro.
- [Deep Learning book (Goodfellow) — caps. 1, 6](https://www.deeplearningbook.org/) —
  teoria de redes neurais e retropropagação.
- [Lotte et al. — EEG-BCI classification](https://doi.org/10.1088/1741-2560/4/2/R01) —
  quando modelos simples bastam em dados neurais.
- [vLLM — docs](https://docs.vllm.ai/) — prefill/decode e batching na prática.