# Desafio — Frequência de Corte de Circuito RC Tecidual

## 1. Objetivo do Desafio
Implementar a rotina de cálculo da frequência de corte a $-3\text{ dB}$ de um circuito passa-baixas equivalente RC biológico a partir da resistência em ohms e capacitância em farads.

## 2. Especificação Técnica e Formulação
Dados a resistência em ohms `r_ohms` e a capacitância em farads `c_farads`:
- Implemente a função `rc_cutoff(r_ohms, c_farads)`:
  $$f_c = \frac{1}{2\pi \cdot r_{\text{ohms}} \cdot c_{\text{farads}}}$$
- Retorne o valor flutuante da frequência de corte em Hertz (Hz).

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que $R > 0$ e $C > 0$. Caso contrário, levante `ValueError`.
- Para $R = 10000\ \Omega$ e $C = 10^{-6}\text{ F}$ ($1\ \mu\text{F}$), o resultado deve ser aproximadamente $15.915\text{ Hz}$.
