# Quantização e ponto fixo

## Ideia

Mapear float → inteiro para caber em menos bits.

Forma afim (Jacob et al. / LiteRT):

`q = round(x / scale) + zero_point`  
`x ≈ scale · (q − zero_point)`

float32 → int8: **4×** menos memória de pesos (1 byte vs 4).

## Fontes primárias

1. **Jacob et al.** — [arXiv:1712.05877](https://arxiv.org/abs/1712.05877) (integer-arithmetic-only inference).
2. **LiteRT 8-bit quantization specification** — [Google AI Edge](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec) (o contrato que kernels/hardware implementam).
3. **CMSIS-NN** — declara seguir int8/int16 do ecossistema TFLM ([docs](https://arm-software.github.io/CMSIS-NN/latest/)).

Não use blog de “INT8 tips” como única fonte.

## Restrições que importam no silício

- Ativações: frequentemente int8 em **[−128, 127]**
- Pesos CONV/FC: frequentemente int8 em **[−127, 127]** com **zero_point = 0**
- Bias: muitas vezes **int32** com `scale ≈ input_scale · weight_scale`

## Fixed-point

Sem FPU, MCU pode usar Q-format (`2⁻ⁿ`). Mesma tensão: range × resolução × overflow.

## Tradeoff

Menos memória/banda/latência ↔ possível perda de acurácia. Meça no hardware (golden tests).
