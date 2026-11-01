# Conceito — Geração LLM: prefill e decode

Gerar texto com um transformer é um loop em que o modelo produz **um token por
vez**, realimentando o contexto. Entender esse loop é entender metade das
métricas de inferência (`nt-inf-metrics`).

## 1. Prefill (processamento do contexto)
- O prompt completo entra de uma vez: atenção em **paralelo** sobre `L` tokens.
- É *compute-bound* e paralelizável; produz os primeiros KV (cache de contexto).
- Latência sentida pelo usuário: **TTFT** (time to first token).

## 2. Decode (geração de novos tokens)
- Token a token: no passo `t`, você computa a atenção do último token contra o
  cache (não reprocessa o contexto) e sorteia o próximo.
- É *memory-bound* (domina na geração) e esconde paralelismo — o motivo de
  sistemas agruparem *batch* de usuários (`nt-serving-batching`).
- Latência entre tokens: **ITL** (inter-token latency); vazão: **tokens/s**.

## 3. Amostragem do próximo token
- Logits de saída → distribuição via softmax; estratégias:
  - **Greedy**: argmax (determinístico);
  - **Top-k / top-p**: restringem o vocabulário sorteado;
  - **Temperature `T`**: `logits/T` — T alto = mais aleatório, T baixo = mais
    agudo (peaking na escolha provável).

## 4. TTFT × throughput (o trade-off clássico)
```
TTFT ~ prefill;  ITL & tokens/s ~ decode
Prefill maior  → melhor throughput, mais memória
Batch maior    → melhor throughput de tokens/s, pior TTFT por requisição
```
Decidir esse balanço é o problema do scheduler do servidor de inferência.

## O que a próxima sala assume
`nt-kv-cache` é a peça de hardware/software que faz o decode possível:
guardar K/V do prefill para o decode não recomputar.

## Leituras recomendadas
- [HF — generation strategies](https://huggingface.co/docs/transformers/en/generation_strategies)
- [NVIDIA — LLM inference guide](https://docs.nvidia.com/deeplearning/frameworks/llm-inference-guide/)
- [vLLM — automatic prefix caching (prefill cache)](https://docs.vllm.ai/en/latest/design/automatic_prefix_caching.html)