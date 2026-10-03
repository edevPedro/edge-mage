# Conceito — Campo Elétrico, Distância e Fontes Profundas

## 1. Fundamento Físico e Lei de Decaimento Dipolar
No condutor de volume biológico sob regime quase-estático, geradores neurais macroscópicos coerentes comportam-se como **dipolos de corrente**.

O potencial elétrico $V$ registrado por um eletrodo à distância $r$ de um dipolo de corrente de momento $p = I \cdot d$ decai com o quadrado da distância:

$$V(r) \approx \frac{p \cdot \cos(\theta)}{4\pi \sigma r^2} \propto \frac{1}{r^2}$$

Onde:
- $r$ é a distância euclidiana da fonte ao eletrodo (em metros ou centímetros).
- $\theta$ é o ângulo entre o eixo do dipolo e o vetor posição do eletrodo.
- $\sigma$ é a condutividade média do meio condutor ($\sim 0.33\text{ S/m}$).

### A Comparação Cortical vs Estruturas Profundas
Considere duas fontes neurais com momento dipolar idêntico:
1. **Fonte Cortical Superficial**: Localizada nos giros corticais a uma distância $d_{\text{cortical}} \approx 1.5\text{ cm}$ do eletrodo de escalpo mais próximo.
2. **Fonte Subcortical Profunda**: Localizada no hipocampo, amígdala ou núcleos da base a uma distância $d_{\text{profunda}} \approx 7.5\text{ cm}$ do escalpo.

A relação de atenuação puramente geométrica é dada pela razão quadrática:
$$\text{Razão} = \left(\frac{d_{\text{cortical}}}{d_{\text{profunda}}}\right)^2 = \left(\frac{1.5}{7.5}\right)^2 = (0.2)^2 = 0.04 = 4\%$$

Se a fonte cortical gera um sinal límpido de $25\ \mu\text{V}$ no escalpo:
$$V_{\text{profunda}} = 25\ \mu\text{V} \times 0.04 = 1.0\ \mu\text{V}$$

Com um piso de ruído biológico e instrumental típico de escalpo de $1.5\ \mu\text{V}_{\text{RMS}}$ (ruído térmico Johnson dos eletrodos + atividade muscular basal do pescoço e couro cabeludo):
$$\text{SNR}_{\text{profunda}} = \frac{1.0\ \mu\text{V}}{1.5\ \mu\text{V}} \approx 0.667 \implies \text{SNR (dB)} = 20 \log_{10}(0.667) \approx -3.52\text{ dB}$$

Como a SNR é negativa e inferior ao limiar mínimo de detecção linear ($\text{SNR} \ge 2.0$, equivalente a $+6\text{ dB}$), a atividade da estrutura profunda fica completamente mascarada sob o ruído de fundo.

Este fenômeno foi extensamente revisado em guias de imageamento de fontes EEG ([Michel & Brunet, PMC6700197](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/)).

## 2. Modos de Falha Operacionais
1. **Promessas de "Decodificar Amígdala/Hipocampo via EEG de Escalpo"**: Afirmar que uma touca de EEG de consumo consegue detectar diretamente emoções subcorticais profundas ou memórias hipocampais em ensaios individuais (*single-trial*). Estruturas profundas requerem eletrodos intracranianos (sEEG, DBS) ou milhares de repetições com médias sincronizadas por estímulo (ERP).
2. **Confundir Atenuação de Carga Estática ($1/r$) com Dipolo de Corrente ($1/r^2$)**: Cargas monopolares isoladas decaem com $1/r$. Como correntes biológicas no meio condutor sempre fecham loops de corrente através de fontes e sumidouros emparelhados (*sinks* e *sources*), o campo resultante é dipolar ($1/r^2$) ou quadrupolar ($1/r^3$).

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-elec-circuit-fundamentals`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/70-nt-elec-circuit-fundamentals/room.yaml)) assume que você compreende as magnitudes dos potenciais biológicos superficiais ($10\text{--}100\ \mu\text{V}$) e investiga as leis fundamentais de circuitos elétricos (Ohm, Kirchhoff, impedância AC) que regem sua medição no hardware.
