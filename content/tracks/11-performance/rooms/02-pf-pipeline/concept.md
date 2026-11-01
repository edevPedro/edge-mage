# Conceito — Pipeline e ILP

Um processador moderno sobrepõe estágios (fetch/decode/execute/memory/writeback). O custo de um *stall* aparece como CPI efetivo > ideal.

## Hazards

| Tipo | Causa | Mitigação típica |
|------|-------|------------------|
| Structural | Recurso compartilhado | Duplicar unidades / ports |
| Data | Dependência RAW/WAR/WAW | Forwarding, renaming, stall |
| Control | Branches | Predição, delay slots (históricos), speculative fetch |

## ILP vs throughput

*Instruction-level parallelism* extrai independência entre instruções. Em kernels de array, o gargalo costuma migrar para **memória** — daí o próximo pilar (cache/TLB) e Roofline depois.

## O que medir

Antes de "otimizar com NEON", pergunte: o código está *latency-bound* no pipeline ou *bandwidth-bound* na hierarquia? Contadores e Roofline respondem; chute não.

