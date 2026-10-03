# Conceito — O Tecido Biológico como Rede RC e Filtragem Passa-Baixas

A estrutura física das membranas celulares e meios intersticiais confere aos tecidos propriedades elétricas complexas que atuam como filtros passa-baixas naturais.

## 1. A Biofísica da Membrana Celular
- **Resistência ($R$):** Determinada pela condutividade iônica do meio extracelular e pela permeabilidade de canais proteicos na membrana.
- **Capacitância ($C$):** A bicamada lipídica atua como um dielétrico hidrofóbico fino (capacitância específica $C_m \approx 1\ \mu\text{F}/\text{cm}^2$).

## 2. A Constante de Tempo ($\tau = RC$) e Frequência de Corte
A resposta ao degrau de tensão de uma membrana biológica segue a equação diferencial de primeira ordem:
$$\tau \frac{dV}{dt} + V = V_0, \quad \tau = R \cdot C$$
A frequência de corte a $-3\text{ dB}$ desse filtro passa-baixas é:
$$f_c = \frac{1}{2\pi \tau} = \frac{1}{2\pi R C}$$
- Frequências acima de $f_c$ sofrem atenuação progressiva de $20\text{ dB/década}$.
- Potenciais de ação ultrarrápidos (spikes com duração de $1\text{ ms}$, equivalentes a frequências $> 500\text{ Hz}$) são fortemente amortecidos pela capacitância da membrana e do tecido circundante ao se propagarem a distância.

## 3. Modos de Falha na Prática de Engenharia
1. **Ignorar o Efeito Capacitivo Tecidual:** Supor que biopotenciais em alta frequência se propagam sem perda de fase ou amplitude através do córtex.
2. **Confundir Capacitância de Membrana com Eletrodo:** A interface eletrodo-gel possui sua própria rede RC de dupla camada eletroquímica, em série com a rede tecidual.

## O Que a Próxima Sala Assume
A próxima sala (`nt-spike-lfp`) — **Spike → LFP (intuição)** — diferencia a dinâmica de potenciais de ação unitários extracelulares e potenciais de campo locais gerados por correntes sinápticas dendríticas.

## Artigos de Apoio e Leituras Recomendadas
- [Einevoll et al. LFP review (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3884846/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Buzsáki et al. LFP (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4907333/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
