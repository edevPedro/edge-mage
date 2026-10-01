# Álgebra linear intro

Matrizes transformam vetores: **y = Ax**. Cada linha de A é um produto escalar com x — a mesma operação de uma camada densa (+ bias).

## 2×2

```
| a b |   |x|   |a·x + b·y|
| c d | · |y| = |c·x + d·y|
```

## Normas

- **L2** (euclidiana): `‖v‖₂ = √(Σ vᵢ²)` — comprimento geométrico
- **L1**: `‖v‖₁ = Σ |vᵢ|` — comum em sparsidade / regularização

Produto escalar: `a·b = Σ aᵢ bᵢ`. Se ambos unitários, `a·b = cos θ`.

## Transposta

`(Aᵀ)ᵢⱼ = Aⱼᵢ`. Em y = xW (batch row-major) vs y = Wx, a convenção muda — mas o custo de GEMM é o mesmo na ordem de grandeza.

## Identidade e camada

Ix = x. Uma densa `y = Wx + b` é matmul + bias: o coração do custo de redes fully-connected no edge.
