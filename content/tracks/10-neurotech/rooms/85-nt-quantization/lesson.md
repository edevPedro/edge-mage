# Desafio — PTQ simétrico: escala, ida e volta

## 1. Objetivo do Desafio
Implementar a cadeia completa de quantização simétrica int8: escala, conversão
para inteiro com clamp, reconstrução e medição do erro ponto-a-ponto.

## 2. Especificação Técnica e Formulação
- `q8_scale(min_val, max_val)` → `max(|min_val|, |max_val|) / 127.0`.
- `quantize_q8(x, scale)` → `[max(-127, min(127, round(v / scale))) for v in x]`.
- `dequantize(q, scale)` → `[q_i * scale for q_i in q]`.
- `quantization_error(x, scale)` → `[abs(x_i − d_i) for (x_i, d_i) em
  zip(x, dequantize(quantize_q8(x, scale), scale))]`.

## 3. Critérios de Validação e Armadilhas
- `round` usa arredondamento de Python (meio-para-par); ok para o lab.
- Clamp é obrigatório fora de [-127, 127] (na verdade a escala é escolhida
  para não estourar, mas proteja o abs).
- Erro exato 0 quando `v` é múltiplo exato de `scale` (teste: 3.0/0.03=100).