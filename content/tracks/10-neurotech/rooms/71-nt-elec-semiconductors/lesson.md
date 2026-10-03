# Desafio — Grampeamento de Tensão por Diodos de Proteção ESD

## 1. Objetivo do Desafio
Implementar a rotina analítica de grampeamento de tensão de entrada (ESD Clamp) simulando o comportamento de corte de diodos semicondutores ideais conectados aos trilhos de alimentação.

## 2. Especificação Técnica e Formulação
Dados a tensão transitória de entrada `v_in`, a tensão do trilho positivo `v_pos_rail`, a tensão do trilho negativo `v_neg_rail` e a queda de condução direta do diodo `v_diode` (todas em Volts):
- Implemente a função `esd_clamp(v_in, v_pos_rail, v_neg_rail, v_diode)`:
  - Limite superior: $V_{\max} = v_{\text{pos\_rail}} + v_{\text{diode}}$.
  - Limite inferior: $V_{\min} = v_{\text{neg\_rail}} - v_{\text{diode}}$.
  - Se $v_{\text{in}} > V_{\max}$: retorne $V_{\max}$.
  - Se $v_{\text{in}} < V_{\min}$: retorne $V_{\min}$.
  - Caso contrário: retorne $v_{\text{in}}$.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que $V_{\text{pos}} > V_{\text{neg}}$ e $V_{\text{diode}} \ge 0$.
- Para trilhos de $+2.5\text{ V}$ e $-2.5\text{ V}$ com diodo de $0.7\text{ V}$, qualquer surto de $10.000\text{ V}$ deve ser rigorosamente grampeado em $+3.2\text{ V}$.
