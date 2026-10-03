# Conceito — Bancos de Filtros Espectrais e Filtragem Notch

O sinal de EEG bruto é um somatório de oscilações biológicas, ruídos fisiológicos e interferência eletromagnética ambiental. O banco de filtros (Filter Bank) é a primeira linha de defesa analítica para isolar os componentes relevantes.

## 1. O Fundamento de DSP em Neuroengenharia
Um banco de filtros consiste em um conjunto de filtros passa-faixa paralelos que decompõem o sinal $x[n]$ em múltiplos sub-sinais $x_k[n]$, cada um restrito a uma banda de interesse:
$$x_k[n] = h_k[n] * x[n]$$

Onde $h_k$ representa a resposta ao impulso do filtro para a $k$-ésima banda (por exemplo, sub-bandas de $4	ext{ Hz}$ de largura cobrindo de $4	ext{ a }32	ext{ Hz}$, como no algoritmo FBCSP).

### Filtragem Notch (Rejeita-Faixa)
A rede elétrica induz correntes capacitivas no corpo humano que geram potenciais de $50	ext{ Hz}$ (Europa/Ásia) ou $60	ext{ Hz}$ (Américas). O filtro notch é projetado com zeros no círculo unitário em $\omega_0 = 2\pi f_0 / f_s$ para introduzir atenuação profunda ($> 40	ext{ dB}$) em uma vizinhança estreita sem distorcer as frequências vizinhas.

### O Limite de Nyquist-Shannon
A taxa de amostragem $f_s$ impõe o limite superior estrito para o conteúdo de frequência sem aliasing:
$$f_{\text{Nyquist}} = \frac{f_s}{2}$$
Para $f_s = 250\text{ Hz}$, nenhuma frequência útil ou ruído acima de $125\text{ Hz}$ pode ser processada digitalmente sem causar rebatimento espectral destrutivo.

## 2. Unidades e Ordens de Grandeza
- **Frequência de amostragem ($f_s$):** $250\text{ Hz}$ (padrão comum em OpenBCI e sistemas móveis).
- **Interferência de rede:** $50\text{ ou } 60\text{ Hz}$ (amplitudes de $50\text{ a } 500\ \mu\text{V}$).
- **Largura típica de bandas de BCI:** $\Delta f = 2\text{--}4\text{ Hz}$ para filtros sub-banda.

## 3. Modos de Falha na Prática de Engenharia
1. **Filtro com Fator Q Excessivamente Alto:** Pode causar oscilação prolongada (ringing no domínio do tempo) após transientes abruptos, gerando artefatos artificiais.
2. **Ignorar Nyquist em Amostragem Subsequente:** Tentar subamostrar o sinal (downsampling) sem aplicar um filtro passa-baixas anti-aliasing prévio, causando distorção irreversível das bandas sensoriomotoras.

## O Que a Próxima Sala Assume
A próxima sala (`nt-dsp-welch`) — **DSP — Welch e vazamento espectral** — estima a densidade espectral de potência (PSD) utilizando janelamento e médias de periodogramas com controle de vazamento.

## Artigos de Apoio e Leituras Recomendadas
- [OpenBCI — Setting up for EEG](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Riemannian approaches in BCI (HAL PDF)](https://inria.hal.science/hal-01394253/document) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Ang et al. — Filter Bank Common Spatial Pattern (FBCSP) IEEE](https://doi.org/10.1109/IJCNN.2008.4634130) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
