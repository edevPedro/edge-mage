# Desafio — Atenuação de Ruído de Alimentação por PSRR

## 1. Objetivo do Desafio
Implementar a rotina analítica de cálculo da atenuação em decibéis da Taxa de Rejeição de Fonte de Alimentação (PSRR) a partir da ondulação na fonte e do ruído residual resultante na saída.

## 2. Especificação Técnica e Formulação
Dadas a amplitude de ondulação (ripple) de entrada na fonte `v_ripple_in` em Volts e a amplitude do ruído residual vazado na saída `v_noise_out` em Volts ($V_{\text{in}} > 0, V_{\text{out}} > 0$):
- Implemente a função `psrr_attenuation_db(v_ripple_in, v_noise_out)`:
  $$\text{PSRR} = 20.0 \times \log_{10}\left( \frac{v_{\text{ripple\_in}}}{v_{\text{noise\_out}}} \right)$$
- Retorne o valor flutuante em decibéis (dB).

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que $V_{\text{noise\_out}} > 0$ para evitar divisão por zero ou logaritmo de zero.
- Para uma ondulação de entrada de $0.1\text{ V}$ ($100\text{ mV}$) e ruído na saída de $10^{-5}\text{ V}$ ($10\ \mu\text{V}$), o PSRR deve ser exatamente $20 \log_{10}(10000) = 80.0\text{ dB}$.
