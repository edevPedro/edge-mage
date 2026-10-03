# Desafio — Suavização Exponencial de Comandos de Controle (EMA)

## 1. Objetivo do Desafio
Implementar a rotina de suavização exponencial adaptativa (Exponential Moving Average) para amortecer flutuações estocásticas de decodificadores neurais em malha fechada.

## 2. Especificação Técnica e Formulação
Dado o estado atual suavizado `current` ($y[t-1]$), a nova predição bruta emitida pelo decodificador `target` ($x[t]$), e o fator de suavização $\alpha \in (0, 1]$:
- Implemente a função `ema_update(current, target, alpha)`:
  $$y[t] = \alpha \times \text{target} + (1.0 - \alpha) \times \text{current}$$
- A função deve retornar o novo valor flutuante suavizado $y[t]$.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que se $\alpha = 1.0$, o retorno seja estritamente igual a `target`.
- Se $\alpha = 0.0$, o retorno deve ser estritamente igual a `current`.
