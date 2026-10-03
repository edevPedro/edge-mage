# Lição — Shielding, Layout para Sinais de Microvolts e Power Integrity

## 1. Power Supply Rejection Ratio (PSRR) e Fontes Chaveadas
Em sistemas embarcados alimentados por bateria ou USB, reguladores chaveados (buck/boost) introduzem ripple de comutação na casa de dezenas de milivolts ($10\text{--}50\text{ mV}$).

1. **A Atenuação do PSRR**:
   $$\text{Fator} = 10^{\frac{\text{PSRR (dB)}}{20}}$$
   $$V_{\text{injected}} = \frac{V_{\text{ripple, in}} \times 1000}{\text{Fator}} \quad (\text{em }\mu\text{V})$$
   Se o ripple injetado for superior a $1.0\ \mu\text{V}$, ele consome a faixa dinâmica de entrada e corrompe a relação sinal-ruído de potenciais cerebrais de $10\ \mu\text{V}$.

2. **A Solução por LDO de Baixo Ruído em Cascata**:
   O uso de um LDO com alto PSRR ($>80\text{--}90\text{ dB}$) em cascata após o chaveador atenua o ripple em mais de $30.000\times$, mantendo o ruído injetado abaixo de $0.5\ \mu\text{V}$.

## 2. As Ferramentas de Código Desta Sala
- `psrr_attenuation_db(v_ripple_in, v_ripple_out)`: Calcula a relação analítica de atenuação em decibéis.
- `audit_power_ripple_injection(v_ripple_mv, psrr_db, target_signal_uv, max_injected_uv)`: Modela numericamente o acoplamento do ruído de alimentação no canal de biopotencial, calculando a voltagem induzida em $\mu\text{V}$, a SNR resultante em dB e auditando se o limite do orçamento de ruído ($\le 1.0\ \mu\text{V}$) é respeitado.

Para destravar o lab, abra [TI ADS1299 datasheet](https://www.ti.com/lit/ds/symlink/ads1299.pdf) e leia as recomendações de alimentação e desacoplamento do ADS1299 para o lab de shield/power não tratar ripple como ritmo cerebral.
