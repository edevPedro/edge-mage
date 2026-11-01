# Conceito — Métricas de inferência: o mapa antes da otimização

"Otimizar sem medir" é o erro nº1 em inference engineering. Antes de mexer em
quantização, engine ou batch, defina as métricas e os SLAs.

## 1. As métricas do ciclo de resposta
- **TTFT** (time to first token): atraso até o primeiro token — dominado pelo
  prefill (`nt-llm-generate`).
- **ITL** (inter-token latency): tempo entre tokens — dominado pelo decode.
- **Throughput**: tokens/s (por requisição e agregado em batch).
- **RTF** (real-time factor): tempo de processar 1s de áudio/sinal (crucial
  para loop online BCI: RTF < 1 é obrigatório numa janela contínua).

## 2. Percentis, não médias
- **p50** = experiência típica; **p99/p99.9** = cauda (filas, preemption,
  page faults). SLA de UX trava em p95/p99, não em média.
- Média alta esconde picos; p99 alto destrói fila e frustra usuário.

## 3. Modelo roofline (o "por quê")
Não pergunte "quanto está lento?" — pergunte **"bound por quê?"**:
- **Compute-bound** (ops > bytes trazidos): otimizar com FLOPS/BF16/int8 tensor,
  processos redundantes.
- **Memory-bound** (bytes jogo mais que ops): otimizar com quantização,
  cache-friendly layout, redução de re-leituras.
```
A.I. (arith. intensity) = FLOPs / bytes
Roofline peak = min(compute ≤ peak_ops, memory ≤ peak_BW × A.I.)
```
Prefill do LLM: compute-bound. Decode: memory-bound. Por isso trim(head) em
orçamentos com intervalos diferentes.

## 4. Loop no laboratório BCI
Medir a *própria* pipeline (janela de `n_samples`, features, classificação)
nas mesmas métricas resolve onde o app estoura: aquisição, DSP, ou modelo.

## O que a próxima sala assume
`nt-model-formats`: dado que você *mede*, `nt-model-formats` decide *onde*
servir e em qual formato — runtime e contagem de bytes por camada.

## Leituras recomendadas
- [HF — LLM inference blog (latência/throughput)](https://www.huggingface.co/blog/llm-inference)
- [Roofline model (Berkeley/LLNL)](https://hpc.lbl.gov/publications/roofline-analytical-model)
- [NVIDIA — Nsight Systems (profiling)](https://developer.nvidia.com/nsight-systems)