# Desafio — Cálculo do Ruído Térmico Johnson-Nyquist

## 1. Objetivo do Desafio
Implementar a rotina de cálculo analítico do ruído térmico de tensão RMS gerado por uma resistência ôhmica em temperatura absoluta $T$ sobre uma largura de banda $B$.

## 2. Especificação Técnica e Formulação
Dados a resistência em ohms `r_ohms`, a temperatura em Kelvin `temp_kelvin` e a largura de banda em Hertz `bandwidth_hz`:
- Implemente a função `johnson_noise_v_rms(r_ohms, temp_kelvin, bandwidth_hz)`:
  $$V_{\text{RMS}} = \sqrt{4 \times k_B \times T \times R \times B}$$
  Onde $k_B = 1.380649 \times 10^{-23}\text{ J/K}$.
- Retorne o valor flutuante da tensão RMS de ruído em Volts.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que $R > 0, T > 0, B > 0$. Caso contrário, levante `ValueError`.
- Para $R = 10000\ \Omega, T = 300\text{ K}, B = 100\text{ Hz}$, o ruído térmico deve ser aproximadamente $1.287 \times 10^{-7}\text{ V}$ ($0.129\ \mu\text{V}_{\text{RMS}}$).
