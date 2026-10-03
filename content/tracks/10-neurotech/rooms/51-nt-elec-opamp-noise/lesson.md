# Lição — Op-Amp, Ruído de Entrada e CMRR

## 1. O Orçamento de Ruído do Front-End Analógico
Em biopotenciais não-invasivos, o sinal útil tem amplitude entre $10$ e $100\ \mu\text{V}$. O piso de ruído do amplificador deve ser rigorosamente inferior a $1\ \mu\text{V}_{\text{RMS}}$ sobre toda a banda de aquisição.

1. **Ruído Térmico Johnson-Nyquist**:
   $$V_{n,\text{thermal}} = \sqrt{4 k_B T R_{\text{elec}} \Delta f}$$
   Depende diretamente da impedância de contato do eletrodo $R_{\text{elec}}$. Para $R_{\text{elec}} = 5\text{ k}\Omega$ e $\Delta f = 100\text{ Hz}$, $V_{n,\text{thermal}} \approx 91\text{ nV}_{\text{RMS}}$.

2. **Ruído de Tensão do Amplificador ($e_n$)**:
   $$V_{n,\text{amp}} = e_n \sqrt{\Delta f}$$
   No TI ADS1299, $e_n \approx 10\text{ nV}/\sqrt{\text{Hz}}$. Em $\Delta f = 100\text{ Hz}$, $V_{n,\text{amp}} = 100\text{ nV}_{\text{RMS}}$.

3. **Ruído Total Combinado**:
   $$V_{n,\text{total}} = \sqrt{V_{n,\text{thermal}}^2 + V_{n,\text{amp}}^2}$$
   O valor resultante determina a relação sinal-ruído máxima teórica que o conversor pode digitalizar.

## 2. As Funções de Laboratório Desta Sala
- `johnson_noise_voltage(r_ohms, delta_f_hz, temp_kelvin, kb)`: Calcula a voltagem de ruído térmico em Volts.
- `audit_input_referred_noise(r_elec_ohm, en_nv_rt_hz, bandwidth_hz, target_signal_uv)`: Combina em quadratura o ruído térmico do eletrodo com a densidade de ruído do amplificador, computando a SNR em dB contra o sinal alvo e auditando se o orçamento de ruído ($\ge 20.0\text{ dB}$) é atendido.

Para destravar o lab, abra [TI ADS1299 datasheet](https://www.ti.com/lit/ds/symlink/ads1299.pdf) e leia a seção de ruído referido à entrada do datasheet do ADS1299 para a densidade nV/√Hz fechar o orçamento, não um ganho arbitrário.
