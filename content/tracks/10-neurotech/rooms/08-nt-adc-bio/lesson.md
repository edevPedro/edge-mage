# Desafio — Resolução LSB e Quantização em Microvolts

## 1. Objetivo do Desafio
A conversão A/D é o elo físico entre a eletrofisiologia contínua e os algoritmos de software discreto. Sem ganho prévio adequado ou resolução de conversão suficiente (24 bits), o sinal de microvolts desaparece no ruído de quantização.

## 2. Passo a Passo Matemático

### Cálculo de LSB em Microvolts
Para um ADC diferencial de $N$ bits com tensão de referência $V_{\text{ref}}$ (Volts) e ganho programável $\text{PGA}$:
$$\text{lsb\_uv} = \frac{V_{\text{ref}}}{2^{N-1} \times \text{PGA}} \times 10^6$$

### Auditoria de Resolução Contra Sinal Alvo
Dados $V_{\text{ref}}$, $N$, $\text{PGA}$, `target_signal_uv` (ex: $10.0\ \mu\text{V}$) e `max_lsb_uv` (ex: $2.0\ \mu\text{V}$):
1. Calcule `lsb_uv = adc_lsb_microvolts(vref_volts, n_bits, pga_gain)`.
2. Se `lsb_uv > max_lsb_uv`:
   retorne `(False, lsb_uv, f"Resolução insuficiente: LSB de {lsb_uv:.2f} µV é muito grosseiro para sinal de {target_signal_uv} µV (teto {max_lsb_uv} µV)")`.
3. Caso contrário:
   retorne `(True, lsb_uv, f"Resolução adequada: LSB de {lsb_uv:.4f} µV permite quantização precisa")`.

Consulte o datasheet do [TI ADS1299](https://www.ti.com/lit/ds/symlink/ads1299.pdf) para especificações de ruído e faixa de ganho.
