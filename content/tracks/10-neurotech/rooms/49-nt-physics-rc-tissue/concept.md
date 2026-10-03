# Conceito — Tecido como Circuito RC e Filtragem de Membrana

## 1. Fundamento Físico e Bioelétrico
A membrana neuronal é formada por uma bicamada lipídica isolante (espessura $\sim 3\text{--}5\text{ nm}$) perfurada por canais iônicos proteicos condutores. Eletricamente, cada unidade de área de membrana celular é modelada como um circuito **RC paralelo**:

| Parâmetro Biofísico | Símbolo | Valor Típico | Unidade SI |
|---|---|---|---|
| **Capacitância Específica da Membrana** | $C_m$ | $\approx 1.0$ | $\mu\text{F/cm}^2$ ($10^{-2}\ \text{F/m}^2$) |
| **Resistência Específica da Membrana** | $R_m$ | $10^3\text{--}10^5$ | $\Omega\cdot\text{cm}^2$ |
| **Constante de Tempo da Membrana** | $\tau_m = R_m C_m$ | $10\text{--}50$ | $\text{ms}$ ($10^{-2}\text{ s}$) |
| **Frequência de Corte Intrínseca** | $f_c = \frac{1}{2\pi \tau_m}$ | $3.2\text{--}15.9$ | $\text{Hz}$ |

Este modelo físico, detalhado por [Einevoll et al. (PMC3884846)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3884846/) e [Buzsáki et al. (PMC4907333)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4907333/), estabelece que a membrana atua intrinsecamente como um **filtro passa-baixa analógico de primeira ordem**.

### Derivação da Resposta em Frequência
A reatância capacitiva da membrana é dada por $X_C = \frac{1}{2\pi f C}$. À medida que a frequência $f$ aumenta:
- $X_C \to 0$: a capacitância da membrana oferece caminho de baixíssima impedância para correntes alternadas de alta frequência, drenando-as (*shunting* capacitivo) para o meio intracelular/extracelular sem despolarizar o soma ou gerar potenciais dipolares sustentados.
- A função de transferência do circuito RC paralelo de membrana possui magnitude:

$$|H(f)| = \frac{1}{\sqrt{1 + (2\pi f \tau_m)^2}}$$

E a atenuação em decibéis é:
$$\text{Atenuação (dB)} = 20 \log_{10}(|H(f)|)$$

Com $\tau = 0.01\text{ s}$ ($f_c \approx 15.9\text{ Hz}$):
- Para um ritmo $\alpha/\mu$ de $10\text{ Hz}$:
  $$|H(10)| = \frac{1}{\sqrt{1 + (2\pi \cdot 10 \cdot 0.01)^2}} = \frac{1}{\sqrt{1 + 0.395}} \approx 0.847 \implies -1.45\text{ dB}$$
  O sinal oscilatório passa quase sem atenuação ($<3\text{ dB}$ de perda).
- Para componentes rápidas de um spike de $1000\text{ Hz}$:
  $$|H(1000)| = \frac{1}{\sqrt{1 + (2\pi \cdot 1000 \cdot 0.01)^2}} \approx \frac{1}{62.8} \approx 0.0159 \implies -35.96\text{ dB}$$
  A atenuação é superior a $35\text{ dB}$ (fator de redução de mais de $60\times$), demonstrando por que variações rápidas de potencial não conseguem estabelecer campos elétricos amplos no meio.

## 2. Modos de Falha Operacionais
1. **O Mito do "Cérebro como Resistor Puro"**: Tratar o condutor de volume e as membranas celulares como resistores puramente ôhmicos. Isso faz o desenvolvedor ignorar o atraso de fase capacitivo e o filtro passa-baixa tecidual intrínseco, levando a modelos estáticos incorretos de propagação de campo.
2. **Confundir Impedância de Membrana com Impedância de Eletrodo**: A constante $\tau = R C$ de membrana regula a propagação de correntes transmembrana nos neurônios. Ela não deve ser confundida com a impedância eletrodo-gel-pele tratada nas salas de instrumentação ([`nt-electrode-snr`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/06-nt-electrode-snr/room.yaml)).

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-spike-lfp`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/04-nt-spike-lfp/room.yaml)) assume que você compreende a constante de tempo $\tau = R C$ da membrana e a atenuação seletiva de altas frequências, usando essa base física para diferenciar a propagação de spikes rápidos versus oscilações lentas de LFP.
