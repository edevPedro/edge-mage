# Conceito — Circuitos Elétricos, Leis de Kirchhoff e Impedância AC no AFE

## 1. Fundamento de Circuitos em Biopotenciais
A interface entre o corpo humano e a eletrônica de instrumentação é governada pelas leis fundamentais de circuitos em regime contínuo (DC) e alternado (AC):

| Lei / Conceito | Expressão Matemática | Aplicação em Neurotecnologia |
|---|---|---|
| **Lei de Ohm** | $V = I \cdot R$ | Queda de tensão em resistores e atenuação em divisores |
| **KCL (Nós de Kirchhoff)** | $\sum I_{\text{nó}} = 0$ | Conservação de correntes nos nós de bias e feedback do AFE |
| **KVL (Malhas de Kirchhoff)** | $\sum V_{\text{malha}} = 0$ | Acoplamento de potenciais espúrios em loops de terra (*ground loops*) |
| **Impedância AC** | $Z = R + jX, \quad X_C = \frac{1}{2\pi f C}$ | Comportamento reativo de cabos, pele e desacoplamento |

### O Divisor AC por Capacitância Parasita de Cabo
Em DC, a resistência de entrada dos bioamplificadores modernos (como o [TI ADS1299](https://www.ti.com/lit/ds/symlink/ads1299.pdf)) atinge $1\text{ G}\Omega$, tornando a atenuação resistiva pura desprezível para eletrodos clínicos de $5\text{ k}\Omega$.

Entretanto, em sinais alternados (frequências de EEG de $1\text{--}100\text{ Hz}$ e ruído de rede de $60\text{ Hz}$), cabos longos entre o eletrodo e a placa possuem capacitância parasita em relação ao terra ($C_{\text{cabo}} \approx 50\text{--}150\text{ pF/m}$). Essa capacitância fica em paralelo com a entrada do amplificador, formando um divisor de tensão reativo com a resistência de contato da pele $R_{\text{pele}}$:

$$X_C = \frac{1}{2\pi f C_{\text{cabo}}}$$
$$V_{\text{meas}} = V_{\text{source}} \cdot \frac{X_C}{\sqrt{R_{\text{pele}}^2 + X_C^2}}$$
$$\text{Perda (\%)} = \left(1.0 - \frac{V_{\text{meas}}}{V_{\text{source}}}\right) \times 100\%$$

- **Eletrodo Clínico Úmido ($R_{\text{pele}} = 5\text{ k}\Omega$, $C = 100\text{ pF}$, $f = 60\text{ Hz}$)**:
  $$X_C = \frac{1}{2\pi \cdot 60 \cdot 100\times 10^{-12}} \approx 26.53\text{ M}\Omega$$
  Como $26.53\text{ M}\Omega \gg 5\text{ k}\Omega$, a perda é de apenas $0.00002\%$. O sinal é preservado integralmente.
- **Eletrodo Seco de Alta Impedância ($R_{\text{pele}} = 2\text{ M}\Omega$, $C = 1000\text{ pF}$ cabo longo sem blindagem ativa)**:
  $$X_C = \frac{1}{2\pi \cdot 60 \cdot 10^{-9}} \approx 2.65\text{ M}\Omega$$
  $$V_{\text{meas}} = V_{\text{source}} \cdot \frac{2.65}{\sqrt{2^2 + 2.65^2}} \approx 0.798 \cdot V_{\text{source}}$$
  A perda ultrapassa $20\%$, atenuando drasticamente o sinal de microvolts e introduzindo defasagem dependente da frequência.

## 2. Modos de Falha Operacionais
1. **Ignorar a Reatância Capacitiva em Eletrodos Secos**: Projetar sistemas com eletrodos secos ($Z > 1\text{ M}\Omega$) usando cabos coaxiais passivos normais de um metro. A capacitância do cabo atenua as bandas rápidas do EEG e destrói a rejeição de modo comum do amplificador diferencial antes mesmo do primeiro estágio de ganho. Eletrodos secos exigem eletrodos ativos com buffer bufferizador na própria cabeça (*active electrodes*).
2. **Criar Loops de Terra (*Ground Loops*)**: Conectar o terra analógico do bioamplificador ao terra da rede elétrica e a um computador via USB sem isolamento galvânico. A malha fechada capta correntes induzidas por campos magnéticos ambientais, gerando quedas de tensão espúrias via KVL.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-elec-semiconductors`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/71-nt-elec-semiconductors/room.yaml)) assume que você compreende as leis de Kirchhoff e a impedância AC, aplicando esses conceitos aos componentes não-lineares de proteção de entrada (diodos de clamp ESD e chaves MOSFET).
