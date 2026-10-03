# Desafio — Multiplicação e Acumulação com Saturação Q15

## 1. Objetivo do Desafio
Implementar a rotina fundamental de multiplicação e acumulação com saturação (MAC Q15) representativa do conjunto de instruções de microcontroladores de sinal (DSP), prevenindo o wrap-around de overflow.

## 2. Especificação Técnica e Formulação
Considere a operação de ponto fixo Q15 onde valores válidos estão restritos ao intervalo inteiro $[-32768, 32767]$:
- Implemente a função `q15_mac(acc, a, b)` que recebe o acumulador atual `acc` (inteiro de 32 bits) e dois operandos Q15 `a` e `b`:
  $$\text{produto} = (a \times b) \gg 15$$
  $$\text{novo\_acc} = \text{clamp}(\text{acc} + \text{produto}, -32768, 32767)$$
- Onde $\text{clamp}(v, \text{min}, \text{max})$ garante que valores acima de $32767$ saturem em $32767$, e valores abaixo de $-32768$ saturem em $-32768$.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que o shift à direita por 15 bits normalize o produto de dois valores Q15 de volta para a escala correta de 16 bits.
- A saturação aritmética é mandatória: nunca permita que o acumulador inverta de sinal por overflow modular.
