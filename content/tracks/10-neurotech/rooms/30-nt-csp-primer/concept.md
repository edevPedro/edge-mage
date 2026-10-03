# Conceito — Padrões Espaciais Comuns (Common Spatial Patterns - CSP) e Log-Variância

O algoritmo Common Spatial Patterns (CSP) é a técnica clássica de filtragem espacial supervisionada mais bem-sucedida em interfaces cérebro-computador baseadas em Imagética Motora.

## 1. O Princípio Matemático do CSP
Dadas duas classes de ensaios de EEG multicanal com matrizes médias de covariância normalizada $\Sigma_1$ e $\Sigma_2 \in \mathbb{R}^{C \times C}$:
O CSP busca filtros espaciais lineares $w$ que maximizam a razão de variâncias (quociente de Rayleigh generalizado):
$$J(w) = \frac{w^T \Sigma_1 w}{w^T \Sigma_2 w}$$
Isso é resolvido pelo problema de autovalores generalizados:
$$\Sigma_1 w = \lambda \Sigma_2 w$$
Ou, equivalentemente, diagonalizando simultaneamente a covariância combinada $\Sigma_c = \Sigma_1 + \Sigma_2$ através de branqueamento espacial (whitening).

## 2. Extração de Características por Log-Variância
Dado um ensaio multicanal $X \in \mathbb{R}^{C \times T}$ e um vetor de filtro espacial $w \in \mathbb{R}^C$:
1. O sinal filtrado espacialmente unidimensional é:
   $$s[t] = w^T X[t] = \sum_{c=1}^C w_c X[c, t]$$
2. A variância do sinal projetado ao longo de $T$ amostras é calculada:
   $$\text{Var}(s) = \frac{1}{T - 1} \sum_{t=1}^T (s[t] - \bar{s})^2$$
3. Aplica-se a transformação logarítmica para gaussianizar a distribuição da característica:
   $$f = \log_{10}(\text{Var}(s))$$

Tipicamente, selecionam-se os $m$ primeiros e os $m$ últimos autovetores ($2m$ filtros espaciais, usualmente $m = 2$ ou $3$), formando um vetor de características compacto de dimensão $2m$.

## 3. Modos de Falha na Prática de Engenharia
1. **Vazamento Espacial de Treino:** Ajustar os filtros CSP sobre todos os ensaios da sessão antes de dividir os folds da validação cruzada. Como o CSP é supervisionado, isso produz acurácias espúrias de mais de 90% em dados onde só existe ruído puro!
2. **Matrizes de Covariância Mal-Condicionadas:** Em montagens com muitos eletrodos ($C > 32$) e poucos ensaios, $\Sigma_1$ e $\Sigma_2$ tornam-se singulares. É obrigatório aplicar regularização de encolhimento (Shrinkage) nas matrizes de covariância antes de resolver o CSP (Regularized CSP - RCSP).

## O Que a Próxima Sala Assume
A próxima sala (`nt-riemann-primer`) — **Primer Riemanniano (SPD toy)** — mapeia matrizes de covariância para a variedade riemanniana de matrizes simétricas positivas definidas (SPD) com métrica afim-invariante.

## Artigos de Apoio e Leituras Recomendadas
- [Ramoser et al. IEEE TNSRE 2000 — CSP](https://doi.org/10.1109/86.895946) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Ang et al. FBCSP IJCNN 2008](https://doi.org/10.1109/IJCNN.2008.4634130) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Barachant et al. Riemannian MDM](https://doi.org/10.1109/TBME.2011.2172210) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
