# Conceito — Álgebra Linear

## Matriz × vetor
`(Ax)_i = Σ_j A_{ij} x_j`

## Norma
`‖x‖₂ = √(Σ x_i²)` — distância euclidiana.

## Matmul
`C = AB` com `C_{ik} = Σ_j A_{ij} B_{jk}`.
FLOPs ≈ `2 m n k` para `m×k` · `k×n`.

## Intuição
Rotações, escalas e mudanças de base são matrizes. No edge, matmul é o coração da inferência.
