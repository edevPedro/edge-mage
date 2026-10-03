# Desafio — Conversão de Ponto Flutuante para Q15 com Saturação

## 1. Objetivo do Desafio
Implementar a rotina fundamental de conversão de números fracionários em ponto flutuante para a representação inteira em ponto fixo Q15 com sinal de 16 bits, aplicando proteção estrita de saturação aritmética para evitar descontinuidades de sinal por *wrap-around*.

## 2. Especificação Técnica
Implemente a função `float_to_q15(x)`:
- Multiplique o valor float $x$ pelo fator de escala fracionário $32768.0$ e converta para inteiro arredondado (ou truncado conforme a convenção inteira padrão):
  $$\text{raw} = \text{int}(x \times 32768.0)$$
- Aplique saturação rígida aos limites da faixa de 16 bits com sinal:
  - Se $\text{raw} > 32767$, retorne `32767`.
  - Se $\text{raw} < -32768$, retorne `-32768`.
  - Caso contrário, retorne $\text{raw}$.

## 3. Exemplos Canônicos de Validação
```python
assert float_to_q15(0.5) == 16384
assert float_to_q15(-1.0) == -32768
assert float_to_q15(1.5) == 32767      # Saturação positiva
assert float_to_q15(-2.0) == -32768    # Saturação negativa
```

## 4. Critérios de Validação e Armadilhas
- Garanta que qualquer valor float $\ge 1.0$ sature rigorosamente em `32767`.
- O valor retornado deve ser um tipo inteiro (`int`).
