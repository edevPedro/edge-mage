# Conceito — Amplificador de Instrumentação (INA), Ganho e Saturação por Offset DC

Em eletrofisiologia, o primeiro estágio ativo da cadeia analógica é o Amplificador de Instrumentação (INA). Sua função primária é amplificar biopotenciais diferenciais minúsculos ($10\text{--}100\ \mu\text{V}$) rejeitando a tensão de modo comum da rede elétrica através de uma arquitetura de três amplificadores operacionais.

```text
V_in+ ---+----|\
         |    | >---+--- R1 ---+
         R_G  |/    |          |
         |          |          +---|\
V_in- ---+----|\    |          |   | >--- V_out (G * V_diff)
              | >---+--- R1 ---+---I/
              |/               |
                               R_ref
```

## 1. O Fundamento da Spec do INA e Saturação

### Ganho Clássico por Resistor de Ganho ($R_G$)
No circuito clássico de três ampop (como o INA128/INA118):
$$G = 1 + \frac{2 R_1}{R_G}$$
Com $R_1 = 50\text{ k}\Omega$, um resistor $R_G = 100\text{ k}\Omega$ define $G = 2$; com $R_G = 10\text{ k}\Omega$, $G = 11$.

### O Perigo do Offset Galvânico DC de Meia-Célula
Entre o metal do eletrodo ($\text{Ag/AgCl}$) e os íons de cloro na pele, estabelece-se uma reação de dupla camada eletroquímica que gera um **potencial de meia-célula DC** (offset) de até $\pm 50\text{ mV}$ (e em eletrodos desbalanceados, até $\pm 300\text{ mV}$).

A tensão diferencial total que entra no INA é a soma do sinal biológico AC e do offset galvânico DC:
$$V_{\text{in}} = V_{\text{diff, AC}} + V_{\text{offset, DC}}$$

Se o engenheiro projeta um ganho elevado no primeiro estágio (por exemplo, $G = 100$) alimentando o chip com alimentação unipolar de $3.3\text{ V}$:
$$V_{\text{out}} = 100 \times (0.000020\text{ V} + 0.050\text{ V}) = 100 \times 0.05002\text{ V} \approx 5.002\text{ V}$$
Como a saída do amplificador não pode ultrapassar o trilho de alimentação positivo ($3.3\text{ V} - V_{\text{headroom}} \approx 3.1\text{ V}$), o circuito **satura completamente contra o trilho superior**. O sinal de EEG de $20\ \mu\text{V}$ é ceifado e destruído.

Por essa razão, arquiteturas modernas de biopotenciais mantêm o ganho analógico do primeiro estágio baixo ($G \in [1, 24]$) e utilizam acoplamento AC ou conversores ADC de 24 bits com alto dynamic range para acomodar o offset DC sem saturação.

## 2. Unidades e Grandezas
- **Sinal diferencial AC ($V_{\text{diff}}$):** $\mu\text{V}$.
- **Offset galvânico DC ($V_{\text{offset}}$):** $\text{mV}$ ($10\text{--}300\text{ mV}$).
- **Resistor de ganho ($R_G$):** $\Omega$ ou $\text{k}\Omega$.
- **Trilhos de alimentação ($V_{\text{supply}}$):** Volts ($3.3\text{ V}$ unipolar ou $\pm 2.5\text{ V}$ bipolar).

## 3. Modo de Falha na Engenharia
Configurar ganho analógico excessivo ($G > 50$) no estágio inicial sem filtro passa-altas de bloqueio DC. Qualquer leve deslocamento do eletrodo modula o offset galvânico em alguns milivolts, levando a saída do INA a bater nos trilhos de alimentação durante vários segundos.

## 4. O que a Próxima Sala Assume
A sala seguinte ([`nt-elec-pcb-emc`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/73-nt-elec-pcb-emc/room.yaml)) assume que você compreende as limitações analógicas do INA para projetar o layout de circuito impresso (PCB) e o isolamento contra acoplamentos eletromagnéticos.

## 5. Ponto de Destrave do Lab
Para inspecionar as especificações elétricas do estágio PGA de biopotenciais e o circuito Driven-Right-Leg (DRL / BIAS) ativo, consulte o datasheet do [TI ADS1299](https://www.ti.com/lit/ds/symlink/ads1299.pdf) e a arquitetura de front-end do [OpenBCI Cyton](https://docs.openbci.com/GettingStarted/Boards/CytonGS/).
