# Conceito — Discriminante Linear de Fisher, Shrinkage e o Decodificador MVP

## 1. Fundamento Matemático: O Critério de Fisher e a Fronteira Bayesiana
O Discriminante Linear de Fisher (LDA) é o classificador de referência e cavalo de batalha na literatura de interfaces cérebro-computador não-invasivas (BCI), conforme documentado por [Lotte et al. (DOI 10.1088/1741-2560/4/2/R01)](https://doi.org/10.1088/1741-2560/4/2/R01) e na documentação do [scikit-learn LinearDiscriminantAnalysis](https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html).

### O Critério de Fisher e a Matriz de Dispersão Intra-Classes
Dados os vetores de características $\mathbf{x} \in \mathbb{R}^D$ (por exemplo, as potências logarítmicas dos canais C3 e C4) rotulados em duas classes $y \in \{0, 1\}$ com médias $\boldsymbol{\mu}_0$ e $\boldsymbol{\mu}_1$:
1. A matriz de dispersão inter-classes é:
   $$\mathbf{S}_b = (\boldsymbol{\mu}_1 - \boldsymbol{\mu}_0)(\boldsymbol{\mu}_1 - \boldsymbol{\mu}_0)^T$$
2. A matriz de dispersão intra-classes combinada (*pooled within-class covariance*) com $N_0$ e $N_1$ ensaios é:
   $$\mathbf{S}_w = \frac{1}{N - 2} \left[ \sum_{i \in C_0} (\mathbf{x}_i - \boldsymbol{\mu}_0)(\mathbf{x}_i - \boldsymbol{\mu}_0)^T + \sum_{j \in C_1} (\mathbf{x}_j - \boldsymbol{\mu}_1)(\mathbf{x}_j - \boldsymbol{\mu}_1)^T \right]$$

O vetor de projeção ideal $\mathbf{w}$ que maximiza o quociente de Rayleigh $J(\mathbf{w}) = \frac{\mathbf{w}^T \mathbf{S}_b \mathbf{w}}{\mathbf{w}^T \mathbf{S}_w \mathbf{w}}$ é a solução direta:
$$\mathbf{w} = \mathbf{S}_w^{-1} (\boldsymbol{\mu}_1 - \boldsymbol{\mu}_0)$$

E o limiar de decisão bayesiano ótimo $b$ para classes equiprováveis é o ponto médio projetado:
$$b = -\frac{1}{2} \mathbf{w}^T (\boldsymbol{\mu}_1 + \boldsymbol{\mu}_0)$$
A predição para um novo ensaio $\mathbf{x}$ é dada pelo sinal do hiperplano linear:
$$\hat{y} = \begin{cases} 1, & \text{se } \mathbf{w}^T \mathbf{x} + b \ge 0 \\ 0, & \text{se } \mathbf{w}^T \mathbf{x} + b < 0 \end{cases}$$

### Regularização por Encolhimento (Shrinkage Regularization)
Em calibrações de BCI com poucos ensaios ($N$ pequeno) e alta dimensionalidade $D$, a estimativa amostral empírica $\mathbf{S}_w$ é mal-condicionada ou singular ($|\mathbf{S}_w| \approx 0$). Inverter uma matriz quase singular amplifica drasticamente o ruído e gera pesos $\mathbf{w}$ com variância aberrante.

Para estabilizar a inversão, aplicamos a regularização de Ledoit-Wolf / shrinkage:
$$\boldsymbol{\Sigma}_{\text{reg}} = (1 - \gamma) \mathbf{S}_w + \gamma \left(\frac{\text{tr}(\mathbf{S}_w)}{D}\right) \mathbf{I}$$
Onde $\gamma \in [0, 1]$ é o parâmetro de encolhimento. Ao adicionar uma fração da matriz identidade ponderada pelo traço médio, os autovalores de $\boldsymbol{\Sigma}_{\text{reg}}$ são afastados de zero, garantindo que a inversa $\boldsymbol{\Sigma}_{\text{reg}}^{-1}$ exista e seja numericamente estável.

## 2. Modos de Falha Operacionais
1. **Inversão de Covariância Singular sem Shrinkage**: Treinar um LDA em poucos ensaios sem regularização. Se dois canais apresentarem correlação espúria próxima de 1 ou se o número de ensaios for inferior ao número de variáveis ($N < D$), a matriz de covariância torna-se não-invertível, disparando erros de ponto flutuante `LinAlgError` ou produzindo predições degeneradas.
2. **Ignorar o Desbalanceamento de Classes no Bias $b$**: Se a classe 0 tiver 80 ensaios e a classe 1 tiver apenas 20 ensaios, usar o bias puramente equidistante $b = -0.5 \mathbf{w}^T(\boldsymbol{\mu}_0 + \boldsymbol{\mu}_1)$ causa viés de predição sistemático. O bias bayesiano correto requer o termo de log-prior $\ln(N_1 / N_0)$.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-metrics-offline`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/16-nt-metrics-offline/room.yaml)) assume que você obteve um vetor de predições $\hat{y}$ do classificador LDA no conjunto de teste independente e necessita avaliar o desempenho real usando métricas que descontam o nível de acerto ao acaso (Cohen's Kappa $\kappa$) e calculam a taxa de transferência de informação (Wolpaw ITR).
