# Conceito — Potência de Banda (Bandpower) e Distribuição Logarítmica de Features

## 1. Fundamento Matemático: Da Oscilação à Energia de Banda
Após a filtragem passa-banda causal realizada pelo estágio biquad, a extração de características em interfaces cérebro-computador baseadas em Imagética Motora (MI-BCI) baseia-se na quantificação da energia espectral instantânea nos canais do córtex sensório-motor primário (eletrodos C3 e C4 do sistema 10-20).

### A Potência Média no Tempo
Para uma janela de tempo de $N$ amostras discretas $x[n]$ filtradas na banda de interesse (ex: ritmo $\mu$ de $8\text{--}12\text{ Hz}$):
$$P = \frac{1}{N} \sum_{n=0}^{N-1} x[n]^2$$

Como a energia de um sinal oscilatório é quadrática, a potência $P$ é estritamente não-negativa ($P \ge 0$).

### A Necessidade da Transformação Logarítmica
Na eletrofisiologia cerebral, as amplitudes espectrais do EEG seguem uma distribuição assimétrica fortemente inclinada à direita (distribuição log-normal ou $\chi^2$ com poucos graus de liberdade). Classificadores lineares como o Discriminante Linear de Fisher (LDA) assumem que as características de cada classe são distribuídas normalmente (gaussianas multivariadas) com matrizes de dispersão compartilhadas.

Para estabilizar a variância e simetrizar a distribuição, aplicamos a transformação logarítmica:
$$f = \log_{10}(P)$$

Para um ensaio (*trial*) multicanal com os eletrodos contralaterais C3 (representação do membro superior direito) e C4 (representação do membro superior esquerdo), o vetor de características bidimensional é:
$$\mathbf{x} = \begin{bmatrix} \log_{10}(P_{C3}) \\ \log_{10}(P_{C4}) \end{bmatrix}$$

Durante a imagética motora da mão direita, ocorre dessincronização relacionada a evento (ERD - Event-Related Desynchronization) no córtex motor esquerdo (C3), reduzindo a potência mu em C3 em relação a C4 ($P_{C3} < P_{C4} \implies \log_{10}(P_{C3}) < \log_{10}(P_{C4})$). Na imagética da mão esquerda, o inverso ocorre no hemisfério direito (C4).

Essa formulação canônica foi revisada por [Padfield et al. (PMC6471241)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) e [Lotte et al. (DOI 10.1088/1741-2560/4/2/R01)](https://doi.org/10.1088/1741-2560/4/2/R01).

## 2. Modos de Falha Operacionais
1. **Entrada de Potência Nula ou Negativa no Logaritmo**: Se um canal estiver desconectado, contiver zeros contínuos ou ocorrer um artefato de saturação matemática onde $P \le 0$, a função $\log_{10}(P)$ colapsa para $-\infty$ ou gera erro de domínio `ValueError`. Em pipelines robustos de produção, deve-se validar $P > 0$ ou utilizar um piso de estabilização $\epsilon$ ($P + \epsilon$).
2. **Normalização Prévia com Vazamento de Dados (Leakage)**: Calcular média e desvio padrão globais sobre todo o banco de ensaios (treino e teste combinados) para normalizar os vetores de features antes de entregá-los ao classificador. Essa prática viola a causalidade estatística e infla artificialmente os resultados de acurácia.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-cv-leakage`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/29-nt-cv-leakage/room.yaml)) assume que você dispõe de vetores de features de potência logarítmica $\mathbf{x} \in \mathbb{R}^2$ para cada ensaio rotulado, e estuda como realizar a partição em blocos temporais independentes (Blocked Cross-Validation) para impedir vazamento de correlação entre janelas vizinhas.
