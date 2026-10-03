# Conceito — Blindagem Eletrostática, Layout para Sinais de Microvolts e Power Integrity

## 1. Integridade de Potência (Power Integrity) e Rejeição de Fonte (PSRR)
Sinais de EEG possuem amplitudes típicas na faixa de $10\text{--}100\ \mu\text{V}$. Fontes de alimentação chaveadas (conversores buck ou boost DC-DC) introduzem ondulação de tensão (*ripple*) e ruído de chaveamento de alta frequência ($100\text{ kHz}\text{--}2\text{ MHz}$) com amplitudes típicas de $10\text{--}50\text{ mV}_{\text{pico}}$.

A capacidade de um circuito integrado de front-end analógico (como o [TI ADS1299](https://www.ti.com/lit/ds/symlink/ads1299.pdf)) de isolar suas saídas analógicas de perturbações presentes nos trilhos de alimentação é medida pela **Razão de Rejeição de Fonte de Alimentação (PSRR - Power Supply Rejection Ratio)**:

$$\text{PSRR (dB)} = 20 \log_{10}\left(\frac{V_{\text{ripple, in}}}{V_{\text{ripple, out}}}\right)$$

O fator de atenuação linear do ruído é:
$$\text{Fator} = 10^{\frac{\text{PSRR (dB)}}{20}}$$

E a tensão de ripple injetada diretamente no canal analógico é:
$$V_{\text{injected}} = \frac{V_{\text{ripple, in}} \times 1000}{\text{Fator}} \quad (\text{em }\mu\text{V})$$

### O Perigo do Regulador Chaveado Direto
Embora o PSRR de amplificadores operacionais e AFEs seja muito alto em corrente contínua ($>100\text{ dB}$ em $0\text{ Hz}$), ele decai progressivamente com a frequência:
- Se alimentarmos o AFE diretamente com um conversor chaveado com $V_{\text{ripple}} = 30\text{ mV}$ em uma frequência onde o PSRR do chip é de apenas $50\text{ dB}$:
  $$\text{Fator} = 10^{50/20} = 10^{2.5} \approx 316.2$$
  $$V_{\text{injected}} = \frac{30.000\ \mu\text{V}}{316.2} \approx 94.87\ \mu\text{V}$$
  Para um sinal EEG biológico de $10\ \mu\text{V}$:
  $$\text{SNR} = \frac{10.0}{94.87} \approx 0.105 \implies \text{SNR (dB)} \approx -19.5\text{ dB}$$
  O ruído de ripple da fonte é dez vezes maior que o sinal cerebral! O conversor analógico-digital digitaliza apenas o chaveamento da fonte.

- Com topologia adequada: inserção de um regulador linear LDO de ultra-baixo ruído e alto PSRR (ex: TI TPS7A47 ou LP5907) em cascata após o chaveador, o ripple é reduzido para $10\text{ mV}$ e o PSRR combinado do sistema atinge $90\text{ dB}$ ($\text{fator} \approx 31.622,8$):
  $$V_{\text{injected}} = \frac{10.000\ \mu\text{V}}{31.622,8} \approx 0.316\ \mu\text{V} \le 1.0\ \mu\text{V}$$
  $$\text{SNR} = \frac{10.0}{0.316} \approx 31.6 \implies +30.0\text{ dB}$$
  O sinal de microvolts emerge límpido sobre o piso de ruído.

## 2. Blindagem e Layout de Placa de Circuito Impresso (PCB)
No design físico para biopotenciais, seguir as diretrizes da documentação da [OpenBCI (EEG Hardware Setup)](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/) é obrigatório:
1. **Particionamento de Domínios**: Separar fisicamente a seção analógica quieta ($AVDD/AGND$) da seção digital ruidosa ($DVDD/DGND$). Não rotear sinais de clock SPI sob as entradas diferenciais do AFE.
2. **Blindagem Ativa (Driven Shield / Guard Ring)**: O cabo do eletrodo é envolvido por uma malha condutora polarizada exatamente com a mesma tensão de modo comum do sinal (usando um buffer seguidor de ganho unitário). Como não há diferença de potencial entre o condutor central e a malha, a corrente capacitiva de fuga é anulada ($I = C \frac{dV}{dt} = 0$).

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-rhythms`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/09-nt-rhythms/room.yaml)) assume que a cadeia de hardware (eletrodos, proteção, amplificação diferencial, terra e alimentação limpa) entrega um sinal analógico estável de microvolts, permitindo iniciar o processamento espectral dos ritmos cerebrais endógenos ($\delta, \theta, \alpha, \beta, \gamma$).
