# Lição — Compatibilidade Eletromagnética e Área de Loop

## 1. Contexto Operacional
Na engenharia de sinais bioelétricos de microvolts, os condutores não são apenas conexões lógicas: são antenas magnéticas que obedecem à Lei de Indução de Faraday. A área geométrica delimitada pelo condutor de sinal e seu retorno à terra determina diretamente a amplitude do ruído induzido.

## 2. Passo a Passo Matemático

### Lei de Indução de Faraday
$$V = -A \times \frac{dB}{dt}$$

### Auditoria de Acoplamento por Loop Magnético
Dados a área do laço `loop_area_cm2` ($\text{cm}^2$), a densidade de fluxo magnético `b_field_ut` ($\mu\text{T}$), a frequência `freq_hz` (Hz) e a amplitude típica do biopotencial `max_eeg_signal_uv` (ex: $15.0\ \mu\text{V}$):
1. Calcule a tensão de pico induzida em microvolts:
   $$V_{\text{ind\_uv}} = \text{loop\_area\_cm2} \times 10^{-4} \times 2 \pi \times \text{freq\_hz} \times \text{b\_field\_ut}$$
2. Se $V_{\text{ind\_uv}} > \text{max\_eeg\_signal\_uv}$:
   retorne `(False, v_ind_uv, f"Ruído induzido ({v_ind_uv:.2f} µV) excede sinal EEG ({max_eeg_signal_uv} µV)")`.
3. Caso contrário:
   retorne `(True, v_ind_uv, f"Área de loop sob controle ({v_ind_uv:.2f} µV < {max_eeg_signal_uv} µV)")`.

Consulte o datasheet do [TI ADS1299](https://www.ti.com/lit/ds/symlink/ads1299.pdf) para as recomendações de roteamento diferencial e stackup de 4 camadas.
