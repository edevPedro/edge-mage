# Desafio — Campo Elétrico a partir do Gradiente de Potencial

## 1. Objetivo do Desafio
Implementar a rotina de cálculo do campo elétrico unidimensional a partir da diferença de potencial entre dois eletrodos separados por uma distância geométrica conhecida.

## 2. Especificação Técnica e Formulação
Dados os potenciais elétricos `v1` e `v2` em Volts e a distância `distance_m` em metros ($d > 0$):
- Implemente a função `electric_field_from_potential(v1, v2, distance_m)`:
  $$E = \frac{v_1 - v_2}{\text{distance\_m}}$$
- Retorne o valor flutuante do campo elétrico em Volts por metro (V/m).

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que a distância seja estritamente positiva ($d > 0$). Caso contrário, levante `ValueError`.
- A convenção de sinal deve respeitar o sentido do gradiente: $E > 0$ se $V_1 > V_2$.
