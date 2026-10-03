# Conceito — Referência, Terra e Conversão de Modo Comum

Em sistemas bioelétricos, o corpo humano atua como uma antena que capta campos elétricos da rede de distribuição de energia ($50\text{ Hz}$ ou $60\text{ Hz}$). Esse acoplamento capacitivo induz tensões de modo comum ($V_{cm}$) de $1\text{ V}$ a $3\text{ V}$ em todo o escalpo do sujeito.

## 1. O Fundamento da Spec de Conversão Modo Comum → Diferencial

### A Ilusão do CMRR Infinito
Muitos desenvolvedores supõem que um amplificador de instrumentação com $\text{CMRR} = 110\text{ dB}$ eliminará completamente o zumbido de $60\text{ Hz}$. Isso só seria verdade se os eletrodos tivessem impedâncias perfeitamente idênticas.

Considere dois eletrodos de entrada (Canal e Referência) com impedâncias de contato $Z_1$ e $Z_2$, conectados a um bioamplificador com impedância de entrada $R_{\text{in}}$:
$$V_1 = V_{cm} \left(\frac{R_{\text{in}}}{Z_1 + R_{\text{in}}}\right), \quad V_2 = V_{cm} \left(\frac{R_{\text{in}}}{Z_2 + R_{\text{in}}}\right)$$

A tensão diferencial espúria resultante antes de qualquer estágio de amplificação é:
$$V_{\text{diff}} = |V_1 - V_2| = V_{cm} \left| \frac{R_{\text{in}}}{Z_1 + R_{\text{in}}} - \frac{R_{\text{in}}}{Z_2 + R_{\text{in}}} \right| \approx V_{cm} \frac{|Z_1 - Z_2|}{R_{\text{in}}}$$

### O Cenário Real de Falha
- Tensão de modo comum acoplada ao corpo: $V_{cm} = 1.0\text{ V}$.
- Impedância de $C3$: $Z_1 = 5\text{ k}\Omega$.
- Impedância da Referência no lóbulo da orelha (gel ressecado): $Z_2 = 25\text{ k}\Omega$ ($\Delta Z = 20\text{ k}\Omega$).
- Se o amplificador tiver $R_{\text{in}} = 100\text{ M}\Omega$:
  $$V_{\text{diff}} = 1.0 \times \frac{20 \times 10^3}{100 \times 10^6} = 2 \times 10^{-4}\text{ V} = 200\ \mu\text{V}$$
- Uma tensão parasita de $200\ \mu\text{V}$ a $60\text{ Hz}$ é dez a vinte vezes maior do que o sinal biológico de interesse ($10\text{--}20\ \mu\text{V}$). O sinal entra no ADC saturando a faixa dinâmica!
- Se $R_{\text{in}} = 10\text{ G}\Omega$ ($10^{10}\ \Omega$):
  $$V_{\text{diff}} = 1.0 \times \frac{20 \times 10^3}{10^{10}} = 2\ \mu\text{V}$$
  O ruído convertido fica abaixo do limiar estrito de tolerância de $5.0\ \mu\text{V}$.

## 2. Unidades e Grandezas
- **Tensão de modo comum ($V_{cm}$):** Volts ($1\text{--}3\text{ V}$ RMS na proximidade de tomadas e cabos AC).
- **Desbalanço de impedância ($\Delta Z = |Z_1 - Z_2|$):** $\text{k}\Omega$.
- **Ruído diferencial convertido ($V_{\text{diff}}$):** $\mu\text{V}$.
- **CMRR:** $\text{dB} = 20 \log_{10}(|G_d| / |G_{cm}|)$.

## 3. Modo de Falha na Engenharia
Acreditar que o filtro notch digital de $60\text{ Hz}$ resolve tudo. Se o ruído diferencial convertido for de $500\ \mu\text{V}$ e o ganho do pré-amplificador for $G = 100$, a saída atinge $50\text{ mV}$ ou satura o ADC, ceifando a forma de onda de forma não linear antes que o DSP digital receba qualquer amostra.

## 4. O que a Próxima Sala Assume
A próxima sala do percurso é `nt-elec-opamp-noise` (Elétrica — Op-amp, ruído e CMRR): Ruído de entrada, ganho e CMRR no AFE bio.

## 5. Ponto de Destrave do Lab
Para entender a interação crítica entre impedância de escalpo e rejeição de modo comum em estudos clínicos, consulte o clássico de [Ferree et al. (DOI 10.1016/S1388-2457(00)00533-2)](https://doi.org/10.1016/S1388-2457(00)00533-2) e as práticas de aterramento e bias da [OpenBCI EEG Setup](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/).
