# Desafio — Impedância de Eletrodos e Divisor de Entrada

## 1. Objetivo do Desafio
O biopotencial de EEG é uma fonte de tensão com altíssima impedância de saída ($Z_{\text{electrode}}$). Se o front-end analógico não possuir uma impedância de entrada ($R_{\text{in}}$) ordens de magnitude maior, a interface sofre atenuação resistiva e distorção espectral severa.

## 2. Passo a Passo Matemático

### SNR em Decibéis
$$\text{SNR}_{\text{dB}} = 10 \times \log_{10}\left(\frac{P_{\text{sinal}}}{P_{\text{ruido}}}\right)$$

### Auditoria do Divisor de Impedância
Dados $Z_{\text{electrode}}$ e $R_{\text{in}}$ em Ohms:
1. Se $R_{\text{in}} \le 0$ ou $Z_{\text{electrode}} < 0$, levante `ValueError`.
2. Calcule o erro percentual de atenuação:
   $$\text{error\_pct} = \frac{Z_{\text{electrode}}}{Z_{\text{electrode}} + R_{\text{in}}} \times 100$$
3. Se $\text{error\_pct} > \text{max\_error\_pct}$:
   retorne `(False, error_pct, f"Atenuação de {error_pct:.2f}% excede spec de {max_error_pct}%")`.
4. Caso contrário:
   retorne `(True, error_pct, "Spec de impedância de entrada atendida")`.

Para destravar o lab, abra [OpenBCI — EEG Setup](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/) e leia a montagem de eletrodo e a faixa de impedância: é ela que fixa Z antes da conta do divisor.
