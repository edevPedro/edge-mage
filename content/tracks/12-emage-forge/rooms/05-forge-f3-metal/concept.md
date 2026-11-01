# Conceito · Forge F3 — foundation before GPU

## Pré-requisitos

- P5 intro: modelo de memória Metal ≠ CUDA (`pf-metal-intro`, `pf-gpu-kernels`)
- Boss Metal com golden (`pf-boss-metal`)
- F2: você já sabe se o kernel é memory/compute-bound na CPU

## O que esta etapa ensina

Por que transferir o mesmo golden para GPU: paralelismo de dados, buffers, e o custo de **movimentar** dados. Se não tiver caminho Metal viável, documente fallback honesto — não invente CUDA no Air.

## Offline

Metal no macOS local. Sem nuvem. CUDA eletiva não é obrigatória.
