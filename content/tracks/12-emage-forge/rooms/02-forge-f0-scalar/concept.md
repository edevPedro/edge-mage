# Conceito · Forge F0 — foundation before the harness

Antes de “otimizar”, você precisa de um **referente correto** e mensurável.

## O que esta etapa ensina (leia antes das tasks)

1. **Golden reference** — uma implementação escalar simples o bastante para auditar à mão em N pequeno.
2. **Harness** — entrada fixa, repetição, wall-time (ou ciclos se tiver), e checagem abs/rel contra o golden.
3. **Contrato de evidência** — máquina, flags, N, mediana/p95; sem isso o número não é ciência.

## Por que vem antes de NEON/Metal/inferência

SIMD e GPU só fazem sentido se você sabe *o que* está acelerando e *como* provar que não quebrou a matemática. F0 é essa âncora.

## M4 / offline

Tudo roda no host ARM64 com compilador local. Sem rede. Sem SVE.
