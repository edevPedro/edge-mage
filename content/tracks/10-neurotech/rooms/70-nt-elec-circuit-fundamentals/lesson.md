# Desafio — Efeito de Carga do Divisor de Tensão de Entrada

## 1. Objetivo do Desafio
Implementar a rotina analítica de cálculo da tensão medida na entrada de um amplificador considerando a impedância interna da fonte/eletrodo e a impedância de entrada do circuito.

## 2. Especificação Técnica e Formulação
Dados a tensão da fonte bioelétrica `v_source` em Volts, a resistência/impedância da fonte `r_source` em ohms e a resistência de entrada do amplificador `r_in` em ohms:
- Implemente a função `measured_voltage(v_source, r_source, r_in)`:
  $$V_{\text{meas}} = v_{\text{source}} \times \frac{r_{\text{in}}}{r_{\text{source}} + r_{\text{in}}}$$
- Retorne o valor flutuante da tensão medida em Volts.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que $r_{\text{source}} \ge 0$ e $r_{\text{in}} > 0$.
- Para $v_{\text{source}} = 100\ \mu\text{V}, r_{\text{source}} = 10\text{ k}\Omega, r_{\text{in}} = 90\text{ k}\Omega$, a tensão medida deve ser exatamente $90\ \mu\text{V}$.
