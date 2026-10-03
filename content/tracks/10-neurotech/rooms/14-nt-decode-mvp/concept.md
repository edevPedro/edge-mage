# Conceito — Classificação Linear (LDA), Regularização de Covariância e Cohen's Kappa

O Discriminante Linear de Fisher (LDA) é o padrão-ouro de eficiência computacional e robustez em BCI não-invasivo de baixa latência.

## 1. O Discriminante Linear de Fisher (LDA)
Dado um vetor de características $x \in \mathbb{R}^D$ (por exemplo, potências de banda logarítmicas), o LDA busca um vetor de projeção $w \in \mathbb{R}^D$ e um escalar de viés $b \in \mathbb{R}$ tais que a regra de decisão seja:
$$\hat{y} = \begin{cases} 1, & \text{se } w^T x + b \ge 0 \\ 0, & \text{se } w^T x + b < 0 \end{cases}$$

Onde os pesos ótimos sob premissa de covariância comum $\Sigma$ entre as classes são dados por:
$$w = \Sigma^{-1} (\mu_1 - \mu_0)$$
$$b = -w^T \left(\frac{\mu_1 + \mu_0}{2}\right) + \ln\left(\frac{P(y=1)}{P(y=0)}\right)$$

## 2. Regularização de Encolhimento (Shrinkage de Ledoit-Wolf)
Em BCI, o número de ensaios de calibração $N$ é tipicamente da mesma ordem de grandeza da dimensionalidade $D$ ($N \approx D$ ou $N < D$). A estimativa empírica de covariância amostral $\Sigma$ torna-se mal-condicionada ou singular.

A regularização de encolhimento substitui $\Sigma$ por uma combinação convexa com um alvo estruturado (matriz identidade escalada pelo traço):
$$\Sigma_{\text{reg}} = (1 - \gamma) \Sigma + \gamma \cdot \frac{\text{tr}(\Sigma)}{D} \mathbf{I}$$
Com $\gamma \in (0, 1]$. Isso condiciona a matriz, garante inversibilidade estrita e reduz dramaticamente a variância dos pesos estimados em amostras pequenas.

## 3. Métrica Cohen's Kappa ($\kappa$)
A acurácia percentual simples é enganosa em classes desbalanceadas ou com poucos ensaios. O coeficiente Kappa de Cohen desconta a concordância esperada pelo acaso:
$$\kappa = \frac{p_o - p_e}{1 - p_e}$$
- $p_o$: Acurácia observada (proporção de acertos).
- $p_e$: Concordância esperada ao acaso ($p_e = 0.5$ em problema binário perfeitamente balanceado).
- $\kappa = 0$: Desempenho equivalente ao lançamento de uma moeda honesta.
- $\kappa = 1$: Classificação perfeita.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-riemann-primer`) estuda a geometria não-euclidiana de matrizes de covariância em variedades Riemannianas.

## 5. Ponto de Destrave do Lab
Para o estudo clássico de regularização em BCI e Discriminante Linear com shrinkage, consulte [Blankertz et al. (NeuroImage 2011, The Berlin Brain-Computer Interface)](https://doi.org/10.1016/j.neuroimage.2011.01.057) e [Ledoit & Wolf (J Multivar Anal 2004)](https://doi.org/10.1016/S0047-259X(03)00096-4).
