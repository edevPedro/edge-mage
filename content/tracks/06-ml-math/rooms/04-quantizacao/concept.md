# Conceito — Quantização

## Afim
`real ≈ (q − zp)·scale` (Jacob / LiteRT).

## Contrato edge
Pesos simétricos ⇒ `zp = 0` em várias ops; CMSIS-NN alinha ao esquema TFLM/LiteRT.

## Fixed-point
Bits fracionários negociam range vs precisão.
