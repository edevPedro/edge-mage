# Conceito · Forge F1 — foundation before NEON

## Pré-requisitos (já devem estar feitos na spine)

- P2: pipeline / cache / AArch64 sob lente de perf (`pf-pipeline` … `pf-aarch64-perf`)
- P3 intro: o que é ASIMD/NEON, load/store vetorial, alinhamento, e por que tiling existe (`pf-neon-intro`, `pf-simd-tiling`)
- Boss ARM Math como prova de que você mediu + golden (`pf-boss-arm-math`)

## O que esta etapa ensina

NEON não é “escrever intrinsics”. É mapear o **mesmo** golden de F0 para vias vetoriais sem mudar a semântica, entendendo:

- largura efetiva do vetor no M4 (NEON; **não** SVE)
- custo de gather/scatter improvisado vs layouts contíguos
- quando o ganho morre no cache (volte ao Conceito de P2)

## Offline

Intrinsics / compilador local. Sem download de SDK extra além do Xcode CLT / clang que você já usa.
