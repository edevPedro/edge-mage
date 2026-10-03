# Conceito — Amplificador de Instrumentação (INA) e Supressão Ativa com Driven Right Leg (DRL)

A aquisição de biopotenciais em ambientes não blindados requer rejeição de modo comum tanto passiva (pelo INA) quanto ativa (pelo circuito DRL).

## 1. O Amplificador de Instrumentação de Três Op-Amps
A topologia canônica utiliza dois amplificadores operacionais de buffer na entrada com resistores de realimentação $R_1$ acoplados a um resistor de ganho central $R_G$, seguidos por um estágio subtrator diferencial com ganho unitário:
$$A_v = 1 + \frac{2 R_1}{R_G}$$
Propriedades essenciais:
- **Ultra-Alta Impedância de Entrada:** As entradas conectam-se diretamente às portas não-inversoras dos op-amps de entrada ($R_{\text{in}} > 10^{10}\ \Omega$).
- **Ajuste de Ganho com Resistor Único ($R_G$):** Permite elevar biopotenciais de microvolts para centenas de milivolts sem desbalancear a simetria resistiva interna do subtrator.

## 2. O Circuito Driven Right Leg (DRL) / Bias Ativo
O acoplamento capacitivo da rede elétrica ($60\text{ Hz}$) injeta correntes na ordem de microamperes no corpo do paciente, gerando uma tensão de modo comum $V_{\text{CM}} = (V_1 + V_2) / 2$.
O circuito DRL:
1. Amostra a tensão média de modo comum $V_{\text{CM}}$.
2. Amplifica e inverte o sinal através de um amplificador integrador com ganho $-A_{\text{drl}}$.
3. Realimenta a corrente invertida de volta no paciente:
   $$V_{\text{CM, efetivo}} = \frac{V_{\text{CM}}}{1 + A_{\text{drl}}}$$
Reduz a interferência de modo comum no corpo em 30 a 50 dB adicionais antes de atingir os eletrodos de medição.

## 3. Modos de Falha na Prática de Engenharia
1. **Desconexão do Eletrodo DRL:** Se o eletrodo DRL se soltar da pele, a malha de realimentação se abre e os canais saturam imediatamente em 60 Hz.
2. **Ganho Excessivo no INA com Offset DC:** Ajustar ganho $\times 1000$ em um estágio analógico único sem desacoplamento DC, fazendo com que o potencial de meia-célula do eletrodo ($\approx 300\text{ mV}$) sature o amplificador na tensão máxima de alimentação ($300\text{ V}$ teóricos contra trilho de $3.3\text{ V}$).

## O Que a Próxima Sala Assume
A próxima sala (`nt-adc-bio`) — **ADC e escala µV** — formaliza a quantização digital em microvolts e o dimensionamento da resolução do conversor analógico-digital de 24 bits.

## Artigos de Apoio e Leituras Recomendadas
- [TI ADS1299 datasheet](https://www.ti.com/lit/ds/symlink/ads1299.pdf) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [OpenBCI — Cyton Getting Started](https://docs.openbci.com/GettingStarted/Boards/CytonGS/) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
