# Conceito — Ruído Térmico Johnson-Nyquist, Densidade de Ruído e CMRR em AFE

A captura de sinais bioelétricos na faixa de microvolts ($10\text{--}100\ \mu\text{V}$) opera próxima aos limites físicos fundamentais da termodinâmica e da eletrônica de semicondutores.

## 1. O Ruído Térmico Johnson-Nyquist
Gerado pela agitação térmica aleatória dos portadores de carga em qualquer elemento resistivo:
$$V_{\text{RMS}} = \sqrt{4 k_B T R B}$$
Onde:
- $k_B = 1.380649 \times 10^{-23}\text{ J/K}$ (constante de Boltzmann).
- $T$: Temperatura em Kelvin (ex. $298.15\text{ K}$ ambiente ou $310.15\text{ K}$ corporal).
- $R$: Resistência ôhmica da fonte/eletrodo em ohms.
- $B$: Largura de banda do sistema em Hertz ($\Delta f$).

Densidade espectral de ruído de tensão térmica:
$$e_t = \sqrt{4 k_B T R} \quad [\text{V}/\sqrt{\text{Hz}}]$$

## 2. Ruído Referido à Entrada (RTI - Referred-to-Input)
O ruído total de um estágio de amplificação biológica combina:
$$e_{n,\text{total}}^2 = e_t^2 + e_{n,\text{amp}}^2 + (i_n \times R)^2$$
- $e_{n,\text{amp}}$: Densidade de ruído de tensão intrínseco do amplificador operacional (deve ser $< 10\text{ nV}/\sqrt{\text{Hz}}$).
- $i_n$: Ruído de corrente de entrada (crítico quando a impedância do eletrodo é alta).

## 3. Taxa de Rejeição de Modo Comum (CMRR)
O corpo humano atua como uma antena que capta tensões de modo comum induzidas pela rede de 60 Hz ($V_{\text{CM}} \approx 100\text{ mV}\text{ a } 1\text{ V}$).
Para extrair um biopotencial diferencial de $20\ \mu\text{V}$ com menos de $1\%$ de erro, o amplificador de instrumentação deve apresentar CMRR:
$$\text{CMRR} = 20 \log_{10}\left( \frac{A_d}{A_{\text{cm}}} \right) \ge 100\text{--}120\text{ dB}$$

## 4. Modos de Falha na Prática de Engenharia
1. **Desbalanceamento de Impedância de Eletrodos:** Se um eletrodo tiver $5\text{ k}\Omega$ e o outro tiver $50\text{ k}\Omega$, o divisor de tensão na entrada converte ruído de modo comum de 60 Hz em sinal diferencial (degradação do CMRR efetivo do sistema).
2. **Largura de Banda Excessiva:** Deixar o front-end analógico aberto até 10 kHz quando o sinal de interesse não ultrapassa 100 Hz, quadruplicando o ruído térmico integrado sem ganho fisiológico.

## O Que a Próxima Sala Assume
A próxima sala (`nt-elec-ina-drl`) — **Elétrica — INA, DRL e bias de paciente** — implementa o circuito de perna direita acionada (Driven Right Leg - DRL) para cancelamento ativo de modo comum.

## Artigos de Apoio e Leituras Recomendadas
- [TI ADS1299 datasheet](https://www.ti.com/lit/ds/symlink/ads1299.pdf) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
