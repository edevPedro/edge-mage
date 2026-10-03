# Conceito — Circuitos Elétricos, Leis de Kirchhoff e o Divisor de Tensão na Interface Eletrodo-Amplificador

A interação entre a impedância do tecido biológico, a interface eletroquímica do eletrodo e o amplificador de instrumentação é governada pelas leis fundamentais de Ohm e Kirchhoff.

## 1. As Leis Fundamentais dos Circuitos
- **Lei de Ohm:** $V = I \times R$, ou em corrente alternada: $V(j\omega) = I(j\omega) \times Z(j\omega)$.
- **Lei de Kirchhoff das Correntes (KCL):** A soma algébrica das correntes em qualquer nó de um circuito elétrico é nula ($\sum I_k = 0$), consequência da conservação de carga elétrica.
- **Lei de Kirchhoff das Tensões (KVL):** A soma das quedas e elevações de potencial elétrico ao longo de qualquer malha fechada é nula ($\sum V_k = 0$).

## 2. O Divisor de Tensão de Entrada do AFE
A tensão biológica $V_S$ gerada no tecido com impedância interna $R_S$ acoplada a um amplificador com impedância de entrada $R_{\text{in}}$ gera a tensão efetivamente lida nos terminais do chip:
$$V_{\text{meas}} = V_S \times \frac{R_{\text{in}}}{R_S + R_{\text{in}}}$$
O erro relativo de atenuação por carga é:
$$\text{Erro} = \frac{V_S - V_{\text{meas}}}{V_S} = \frac{R_S}{R_S + R_{\text{in}}}$$
Para minimizar esse erro abaixo de $1\%$, exige-se estritamente $R_{\text{in}} \gg R_S$.

## 3. Modos de Falha na Prática de Engenharia
1. **Impedância de Entrada Insuficiente:** Usar amplificadores operacionais bipolares com correntes de polarização altas e $R_{\text{in}} \approx 1\text{ M}\Omega$ com eletrodos secos de $500\text{ k}\Omega$, resultando em perda de mais de $33\%$ da amplitude de sinal.
2. **Consumo Excessivo de Potência:** Dimensionar resistores de polarização com valores baixos demais, descarregando rapidamente baterias em dispositivos vestíveis.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-elec-semiconductors`) analisa os componentes semicondutores essenciais para o AFE: diodos de proteção contra descargas eletrostáticas (ESD) e transistores de efeito de campo (MOSFETs).

## 5. Ponto de Destrave do Lab
Consulte o guia clássico de circuitos elétricos de [Nilsson & Riedel (Electric Circuits, Pearson)](https://www.pearson.com/) e [Webster (Medical Instrumentation: Application and Design, Wiley)](https://www.wiley.com/).
