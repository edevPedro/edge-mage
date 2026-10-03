# Conceito — Op-Amp de Biopotencial, Ruído de Entrada e CMRR

## 1. Fundamento e Orçamento de Ruído em Sinais de Microvolts
Na aquisição de sinais EEG de escalpo ($10\text{--}100\ \mu\text{V}$), o piso de ruído do Front-End Analógico (AFE) impõe o limite termodinâmico absoluto da qualidade do decodificador.

O ruído total referido à entrada ($V_{n,\text{total}}$) é a soma em quadratura de duas fontes físicas fundamentais sobre a largura de banda de interesse $\Delta f$ (tipicamente $0.5\text{--}100\text{ Hz}$):

1. **Ruído Térmico Johnson-Nyquist da Interface Eletrodo-Pele**:
   Gerado pela agitação térmica dos portadores de carga na resistência do eletrodo $R_{\text{elec}}$:
   $$V_{n,\text{thermal}} = \sqrt{4 k_B T R_{\text{elec}} \Delta f}$$
   Onde $k_B = 1.38 \times 10^{-23}\ \text{J/K}$ é a constante de Boltzmann e $T \approx 300\ \text{K}$ é a temperatura absoluta.

2. **Ruído de Tensão do Amplificador Operacional / INA**:
   Caracterizado pela densidade espectral de ruído de tensão $e_n$ (expressa em $\text{nV}/\sqrt{\text{Hz}}$):
   $$V_{n,\text{amp}} = (e_n \cdot 10^{-9}) \sqrt{\Delta f}$$

3. **Ruído Total Referido à Entrada**:
   $$V_{n,\text{total}} = \sqrt{V_{n,\text{thermal}}^2 + V_{n,\text{amp}}^2}$$

### Exemplo Numérico com o Circuito Integrado TI ADS1299
O circuito integrado de referência da indústria para biopotenciais, o [TI ADS1299 (datasheet oficial)](https://www.ti.com/lit/ds/symlink/ads1299.pdf), possui densidade de ruído $e_n \approx 10\text{ nV}/\sqrt{\text{Hz}}$ (com ganho de PGA $= 24$):

- Em um contato clínico de qualidade ($R_{\text{elec}} = 5\text{ k}\Omega$, $\Delta f = 100\text{ Hz}$):
  $$V_{n,\text{thermal}} = \sqrt{4 \cdot 1.38\cdot 10^{-23} \cdot 300 \cdot 5000 \cdot 100} \approx 91\text{ nV} = 0.091\ \mu\text{V}$$
  $$V_{n,\text{amp}} = 10\text{ nV}/\sqrt{\text{Hz}} \cdot \sqrt{100\text{ Hz}} = 100\text{ nV} = 0.100\ \mu\text{V}$$
  $$V_{n,\text{total}} = \sqrt{0.091^2 + 0.100^2} \approx 0.135\ \mu\text{V}_{\text{RMS}}$$
  Para um sinal EEG de $10\ \mu\text{V}$:
  $$\text{SNR} = \frac{10.0}{0.135} \approx 74.1 \implies \text{SNR (dB)} = 20 \log_{10}(74.1) \approx 37.4\text{ dB}$$
  O sinal é gravado com excelente relação sinal-ruído ($>30\text{ dB}$).

- Em um eletrodo seco com mau contato ($R_{\text{elec}} = 2\text{ M}\Omega$):
  $$V_{n,\text{thermal}} = \sqrt{4 \cdot 1.38\cdot 10^{-23} \cdot 300 \cdot 2\cdot 10^6 \cdot 100} \approx 1.82\ \mu\text{V}_{\text{RMS}}$$
  Se o sinal cortical sob observação tiver $5\ \mu\text{V}$, a relação sinal-ruído cai para menos de $9\text{ dB}$, deteriorando irreversivelmente as features espectrais antes de qualquer etapa digital.

## 2. Modos de Falha Operacionais
1. **O Mito do "Ganho Infinito Resolve Ruído"**: Desenvolvedores frequentemente aumentam o ganho analógico do amplificador de instrumentação ($G = 1000$ ou $5000$) acreditando que isso "limpa" o sinal. O ganho amplifica tanto o sinal biológico quanto o ruído referido à entrada, aproximando a saída da tensão de saturação dos trilhos de alimentação ($V_{DD} / V_{SS}$).
2. **Ignorar a Densidade Espectral $e_n$**: Escolher amplificadores operacionais comerciais comuns (como LM358, onde $e_n \approx 40\text{--}50\text{ nV}/\sqrt{\text{Hz}}$ e o ruído $1/f$ atinge microvolts na banda lenta de EEG). Biopotenciais exigem amplificadores de instrumentação dedicados ou auto-zero/chopper estabilizados com $e_n \le 15\text{ nV}/\sqrt{\text{Hz}}$.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-elec-ina-drl`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/72-nt-elec-ina-drl/room.yaml)) assume que você compreende o ruído referido à entrada e introduz a topologia de três amplificadores operacionais do Amplificador de Instrumentação (INA) junto com o circuito de acionamento de perna direita (DRL) para cancelamento ativo de modo comum.
