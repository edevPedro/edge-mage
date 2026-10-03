# Desafio — Rejeição de Modo Comum e Desbalanceamento de Impedância

## 1. Objetivo do Desafio
O sinal de EEG é diferencial: medido entre um eletrodo explorador e um eletrodo de referência. O potencial do corpo humano em relação à terra do circuito flutua fortemente devido ao acoplamento com a rede de alimentação de $50/60\text{ Hz}$.

## 2. Passo a Passo Matemático

### Cálculo de CMRR em dB
$$\text{cmrr\_db} = 20 \log_{10}\left(\frac{|G_{\text{diff}}|}{|G_{\text{cm}}|}\right)$$

### Conversão de Modo Comum para Ruído Diferencial
Dados a tensão de modo comum $V_{cm}$ (Volts), impedâncias de contato $Z_1, Z_2$ e impedância de entrada $R_{\text{in}}$ (Ohms):
1. Calcule a atenuação relativa de cada eletrodo:
   $$\alpha_1 = \frac{R_{\text{in}}}{Z_1 + R_{\text{in}}}, \quad \alpha_2 = \frac{R_{\text{in}}}{Z_2 + R_{\text{in}}}$$
2. A tensão diferencial induzida em microvolts é:
   $$V_{\text{diff\_uv}} = V_{cm} \times |\alpha_1 - \alpha_2| \times 10^6$$
3. Se $V_{\text{diff\_uv}} > \text{max\_allowed\_noise\_uv}$:
   retorne `(False, v_diff_uv, f"Ruído de modo comum convertido ({v_diff_uv:.2f} µV) excede limite de {max_allowed_noise_uv} µV")`.
4. Caso contrário:
   retorne `(True, v_diff_uv, f"Ruído diferencial sob controle ({v_diff_uv:.2f} µV)")`.

Consulte [Ferree et al. (2001)](https://doi.org/10.1016/S1388-2457(00)00533-2) para entender as diretrizes de desbalanço máximo de impedância em montagens de biopotenciais.
