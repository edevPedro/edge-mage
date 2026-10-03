# Conceito — Potência de Banda (Bandpower) e Espaço de Características

Em sinais eletrofisiológicos oscilatórios, a amplitude temporal instantânea possui média próxima de zero e fase instável. A potência média de banda (Bandpower) é a representação canônica que quantifica a energia rítmica para decodificação.

## 1. Formulação Matemática da Potência de Banda
Após o sinal ter sido processado por um filtro passa-faixa centrado na banda de interesse (por exemplo, ritmo $\mu$ de $8\text{--}12\text{ Hz}$), a potência média em uma janela de $N$ amostras é a variância do sinal com média zero:
$$P = \frac{1}{N} \sum_{n=0}^{N-1} x[n]^2$$

### A Transformação Logarítmica $\log(P)$
A distribuição das potências estimadas no tempo tende a ser assimétrica e de cauda longa (distribuição qui-quadrado). A aplicação do logaritmo:
$$f = \log_{10}(P) \quad \text{ou} \quad f = \ln(P)$$
produz duas vantagens matemáticas cruciais:
1. **Gaussianização dos Dados:** Aproxima a distribuição das características de uma normal multivariada, satisfazendo a premissa fundamental do Discriminante Linear de Fisher (LDA).
2. **Homogeneização de Variâncias:** Estabiliza a dispersão entre sujeitos com amplitudes basais muito diferentes.

## 2. Unidades e Ordens de Grandeza
- **Sinal de entrada ($x$):** Microvolts ($\mu\text{V}$).
- **Potência de banda ($P$):** Microvolts ao quadrado ($\mu\text{V}^2$).
- **Característica logarítmica ($f$):** Adimensional (escala logarítmica / decibéis relativos).

## 3. Modos de Falha na Prática de Engenharia
1. **Janela Temporal Curta Demais:** Calcular bandpower em janelas menores que 250 ms (para um ritmo de 10 Hz, isso representa menos de 2.5 ciclos), resultando em estimativas de variância instáveis e ruidosas.
2. **Logaritmo de Zero:** Se um canal saturar em zero constante, $\log(0) = -\infty$, quebrando a rotina de classificação numérica. Deve-se garantir um piso de estabilidade $\log(P + \epsilon)$ com $\epsilon = 10^{-10}$.

## O Que a Próxima Sala Assume
A próxima sala (`nt-trial-design`) — **Desenho experimental e trials** — formaliza a sincronização temporal entre estímulos, gatilhos de hardware (triggers) e marcação de épocas neurais.

## Artigos de Apoio e Leituras Recomendadas
- [Yger et al. Riemannian BCI (HAL)](https://inria.hal.science/hal-01394253/document) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Padfield et al. (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Lotte et al. — A review of classification algorithms for EEG-based BCI (IOP)](https://doi.org/10.1088/1741-2560/4/2/R01) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
