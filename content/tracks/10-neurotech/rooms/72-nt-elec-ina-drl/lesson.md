# Desafio — Ganho do Amplificador de Instrumentação (INA)

## 1. Objetivo do Desafio
Implementar a rotina analítica de dimensionamento do ganho de tensão de um amplificador de instrumentação de 3 op-amps a partir do resistor de ganho externo $R_G$ e dos resistores de realimentação $R_1$.

## 2. Especificação Técnica e Formulação
Dados a resistência de ganho em ohms `rg_ohms` e a resistência de realimentação `r1_ohms` (ambas estritamente positivas):
- Implemente a função `ina_gain(rg_ohms, r1_ohms)`:
  $$A_v = 1.0 + \frac{2.0 \times r_{1\text{_ohms}}}{r_{g\text{_ohms}}}$$
- Retorne o valor flutuante do ganho de tensão adimensional.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que $R_G > 0$ e $R_1 > 0$. Se $R_G \le 0$, levante `ValueError`.
- Para $R_1 = 50\text{ k}\Omega$ e $R_G = 1\text{ k}\Omega$, o ganho deve ser exatamente $1 + (100 / 1) = 101.0$.
