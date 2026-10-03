# Conceito — Projeto de Filtros Digitais Causais: IIR (Biquad) vs. FIR e Atraso de Grupo

Em BCI em tempo real, a causalidade temporal é uma restrição inviolável da física dos sistemas.

## 1. O Filtro Biquad IIR (Direct Form II Transposed)
Um filtro de segunda ordem (biquad) em Direct Form II Transposto é definido pela equação de diferenças:
$$y[n] = b_0 x[n] + w_1[n-1]$$
$$w_1[n] = b_1 x[n] - a_1 y[n] + w_2[n-1]$$
$$w_2[n] = b_2 x[n] - a_2 y[n]$$
Onde $w_1$ e $w_2$ são os estados internos do filtro (memória). Os coeficientes são normalizados por $a_0 = 1$.

### Vantagens do IIR:
- Alta seletividade espectral com ordens baixas (ex. ordem 4 ou 6), consumindo poucos ciclos de CPU por amostra.

## 2. Filtros FIR e Atraso de Grupo
Filtros de Resposta ao Impulso Finita (FIR) com coeficientes simétricos possuem fase perfeitamente linear: todas as frequências sofrem exatamente o mesmo atraso de tempo.
O atraso de grupo linear para um filtro FIR com $N$ coeficientes (taps) a uma taxa $f_s$ é:
$$\tau_g = \frac{N - 1}{2 f_s}$$
- Para $N = 65$ e $f_s = 250\text{ Hz}$: $\tau_g = 64 / 500 = 0.128\text{ s} = 128\text{ ms}$.
- Esse atraso consome quase a totalidade do orçamento de latência humana ($< 150\text{ ms}$).

## 3. Modos de Falha na Prática de Engenharia
1. **Instabilidade Numérica de Filtros IIR:** Projetar filtros IIR de ordem alta (ex. ordem 8 direta) sem decomposição em seções de segunda ordem (SOS), fazendo os polos colapsarem fora do círculo unitário por erro de quantização de float32.
2. **Uso de filtfilt em Tempo Real:** Iludir-se com acurácias de filtros de fase zero em testes offline, ignorando que eles são irrealizáveis em hardware de controle contínuo.

## O Que a Próxima Sala Assume
A próxima sala (`nt-artifacts`) — **Artefatos (EOG/EMG/movimento)** — implementa algoritmos de remoção e atenuação de artefatos musculares e oculares que corrompem os traçados corticais.

## Artigos de Apoio e Leituras Recomendadas
- [scipy.signal.firwin](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [TI ADS1299 datasheet (AFE)](https://www.ti.com/lit/ds/symlink/ads1299.pdf) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
