# Conceito — Blindagem Ativa (Driven Shield), Integridade de Alimentação e PSRR

A proteção de biopotenciais frágeis exige controle de ruídos induzidos no cabeamento e isolamento estrito contra ondulações da fonte de alimentação.

## 1. O Princípio da Blindagem Ativa (Driven Shield / Guard Ring)
Em cabos de eletrodos de biopotenciais de alta impedância:
- **Blindagem Aterrada Simples:** A capacitância parasita cabo-terra ($C_{\text{parasita}}$) forma um divisor capacitivo que atenua o sinal biológico e desequilibra o CMRR em frequências acima de 10 Hz.
- **Blindagem Ativa (Driven Shield):** Um amplificador buffer polariza a malha metálica externa com a média de modo comum do sinal interno:
  $$V_{\text{guard}} = V_{\text{CM}}$$
  Pela equação da carga capacitiva $Q = C (V_{\text{sinal}} - V_{\text{guard}})$, como $\Delta V \approx 0$, a corrente capacitiva é anulada ($I = C \frac{dV}{dt} = 0$). Isso cancela o efeito de carga capacitiva do cabo e bloqueia a indução de ruído externo.

## 2. Taxa de Rejeição de Fonte de Alimentação (PSRR)
Fontes de alimentação chaveadas (DC-DC converters) operam com frequências de comutação de centenas de quilohertz, gerando ondulações de tensão (ripple) nos trilhos de alimentação.
O PSRR quantifica a capacidade do amplificador de impedir que variações nos trilhos de energia vazem para a saída do biopotencial:
$$\text{PSRR (dB)} = 20 \log_{10}\left( \frac{\Delta V_{\text{fonte}}}{\Delta V_{\text{saída, ruído}}} \right)$$
- Um PSRR de $80\text{ dB}$ atenua uma ondulação de fonte de $100\text{ mV}$ para apenas $10\ \mu\text{V}$ na saída.
- Para biopotenciais de escalpo, exige-se regulação linear pós-chaveamento com reguladores LDO de ultra-baixo ruído e PSRR $> 70\text{ dB}$.

## 3. Modos de Falha na Prática de Engenharia
1. **Alimentar Front-End Diretamente com USB:** Conectar o conversor ADS1299 diretamente à linha de $+5\text{ V}$ do barramento USB de um computador, injetando milivolts de ruído de clock de placa-mãe diretamente no conversor de 24 bits.
2. **Curto-Circuito em Guard Rings:** Ligar anéis de guarda de PCB na terra do sistema em vez do nó de blindagem ativa, transformando o anel em um capacitor parasita indesejado.

## 4. O que a Próxima Fase Assume
A próxima fase (`nt-neuro-neuron-hh`) inicia o módulo aprofundado de neurociência celular e circuitos neurais de Hodgkin-Huxley e sinapses.

## 5. Ponto de Destrave do Lab
Consulte as notas de aplicação de blindagem ativa e integridade de alimentação biomédica da [Analog Devices (High Impedance Sensors: Driven Shields and Guarding)](https://www.analog.com/) e [Texas Instruments (SBAA206 - Bio-Sensing Front-End Design)](https://www.ti.com/).
