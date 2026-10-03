# Conceito — Geometria Riemanniana e o Cone de Matrizes SPD

O conjunto de matrizes de covariância multicanal estimadas a partir de biopotenciais forma uma variedade diferenciável Riemanniana com curvatura não-positiva, denominada variedade Simétrica Positiva Definida (SPD).

## 1. A Variedade das Matrizes SPD
Uma matriz de covariância $\Sigma \in \mathbb{R}^{C \times C}$ de um sinal multicanal com $C$ eletrodos é:
1. **Simétrica:** $\Sigma = \Sigma^T$.
2. **Positiva Definida:** Para todo vetor não-nulo $v \ne 0$, $v^T \Sigma v > 0$, o que implica que todos os seus autovalores são estritamente positivos ($\lambda_i > 0$).

O espaço de matrizes SPD $\mathcal{S}_{++}^C$ não forma um espaço vetorial, pois a subtração de matrizes SPD pode resultar em matrizes indefinidas ou com autovalores negativos (o que representaria variâncias físicas negativas).

## 2. A Métrica Afim-Invariante (AIRM)
A distância geodésica canônica entre duas matrizes SPD $P_1$ e $P_2$ sob a métrica AIRM é dada por:
$$\delta_R(P_1, P_2) = \|\log(P_1^{-1/2} P_2 P_1^{-1/2})\|_F = \sqrt{\sum_{i=1}^C \ln^2(\lambda_i)}$$
Onde $\lambda_i$ são os autovalores generalizados satisfazendo $P_2 v_i = \lambda_i P_1 v_i$, e $\log(\cdot)$ representa o logaritmo matricial.

### Caso Diagonal Reduzido
Quando as matrizes são diagonais (por exemplo, vetores de potências de canais desacoplados $d_1 = [a_1, \dots, a_C]$ e $d_2 = [b_1, \dots, b_C]$):
$$\delta_{\text{diag}}(d_1, d_2) = \sqrt{\sum_{i=1}^C \left(\ln\left(\frac{a_i}{b_i}\right)\right)^2}$$

## 3. Propriedades e Vantagens em BCI
- **Invariância Afim:** $\delta_R(W P_1 W^T, W P_2 W^T) = \delta_R(P_1, P_2)$ para qualquer matriz invertível $W$. Mudanças lineares de ganho nos eletrodos ou montagens de referência arbitrárias não alteram a distância.
- **Robustez a Ruído e Poucos Ensaios:** O classificador Minimum Distance to Mean (MDM) classifica novas matrizes calculando a distância riemanniana até a média de Fréchet de cada classe, sem exigir a inversão de matrizes empíricas mal-condicionadas.

## 4. Modos de Falha na Prática de Engenharia
1. **Submissão de Matriz Quase Singular:** Se o número de amostras $T < C$, a matriz terá posto reduzido e autovalores nulos, tornando $\ln(\lambda) = -\infty$. É obrigatório aplicar regularização prévia (shrinkage ou regularização de Tikhonov $\Sigma + \epsilon \mathbf{I}$).
2. **Uso de Distância Euclidiana em Matrizes:** A distância Frobenius direta $\|A - B\|_F$ deforma as relações de variância e degrada a separabilidade das classes.

## O Que a Próxima Sala Assume
A próxima sala (`nt-metrics-offline`) — **Acurácia, κ, vazamento de trial** — consolida métricas rigorosas de avaliação offline, matrizes de confusão balanceadas e limites de generalização.

## Artigos de Apoio e Leituras Recomendadas
- [Yger et al. review (HAL PDF)](https://inria.hal.science/hal-01394253/document) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Congedo et al. 2017 primer](https://www.tandfonline.com/doi/full/10.1080/2326263X.2017.1297192) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [arXiv:2407.20250](https://arxiv.org/abs/2407.20250) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Barachant et al. — Multiclass brain–computer interface classification by Riemannian geometry (IEEE)](https://doi.org/10.1109/TBME.2011.2172210) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
