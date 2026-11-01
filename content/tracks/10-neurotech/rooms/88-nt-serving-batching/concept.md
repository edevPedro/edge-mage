# Conceito — Serving & batching: o problema não é o modelo, é a fila

Um modelo rápido não basta: o servidor precisa espremer **tokens/s agregados**
de muitas requisições ao mesmo tempo, mantendo TTFT per-request aceitável. Aqui
entra o scheduler.

## 1. O gargalo do decode no batch
- Cada token novo use uma passada forward (com cache KV). Em um batch (grupo de
  requisições), a GPU processa *mesmos formato* — até o token do mais lento.
- **Static batching**: todas as requisições do batch entram e saem juntas. Como
  saem em momentos diferentes, o batch "espera" a mais longa (a maior
  conversa) — sobra VRAM e latência até para requisições que terminaram.

## 2. Continuous batching (Orca / vLLM / Sarathi)
- O scheduler **interpõe o decode**: cada token gerado derruba a requisição
  como candidata a terminar; terminaram sai, o slot volta ao batch:
  - novas requisições entram no *middle* do decoding;
  - o batch fica sempre cheio → mais tokens/s agregado.
- O trade-off TTFT × throughput volta:

```
batch maior → tokens/s maior, TTFT maior (prefill novo entra no meio)
batch menor → TTFT menor, tokens/s menor
```

## 3. Admissão e SLA
- Como num admission control de BCI online: você **recusa/prioriza** antes de
  prometer ao usuário.
- Critérios: TTFT alvo, fatia do KV cache disponível, prioridade do usuário,
  tolerância a fila; tudo re-evaluado — você mede (`nt-inf-metrics`).

## 4. Analogia BCI
- O loop online já é um scheduler de chunking: janelas entram num pipeline com
  orçamento de latência fixo (RTF < 1). Continuous batching é o mesmo, mas com
  requisições "pacotes de tokens" em vez de amostras contínuas.

## O que a próxima sala assume
`nt-dl-multimodal` (eletiva) encerra o módulo: modelos multimodais (áudio,
imagem, vídeo, sinais) e como a mesma paleta — tokens, atenção, quantização,
batching — serve outras modalidades.

## Leituras recomendadas
- [Continuous batching (Anyscale)](https://www.anyscale.com/blog/continuous-batching-llm-inference)
- [Orca (USENIX OSDI'22)](https://www.usenix.org/system/files/osdi22-yu.pdf)
- [vLLM design docs](https://docs.vllm.ai/en/latest/design.html)