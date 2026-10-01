# Conceito — CMSIS-NN

## Papel
Biblioteca de kernels NN int8/int16 para Cortex-M (DSP / MVE), alinhada ao contrato LiteRT/TFLM.

## Contrato
`real ≈ (q − zp)·scale`. Pesos simétricos em várias ops ⇒ `zp = 0`. Bias int32 com escala composta.

## Classe de CPU
MCU/M-profile → CMSIS-NN (+ TFLM). A-class → ACL / XNNPACK (CMSIS-NN float não é o caminho A).
