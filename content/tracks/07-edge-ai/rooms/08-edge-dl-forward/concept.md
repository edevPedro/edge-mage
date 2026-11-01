# Conceito — Forward DL em int8

## Matmul int8 edge
N×K×M int8 → acumulador **int32**: 127×127×8 ≈ 129k não cabe em int8 a cada passo.

## Escala dupla
`s_out = s_in × s_w` — entrada e peso têm escalas próprias; o resultado int32 vira float/requant no fim.

## Dequant
`real ≈ q · scale` (pesos simétricos: zero-point 0).