# Conceito — Estabilidade Numérica, Aritmética de Ponto Flutuante e Regularização

## 1. Aritmética de Ponto Flutuante e Cancelamento Catastrófico
Em processadores digitais de sinais e computadores padrão (IEEE 754):
- Números em `float32` possuem apenas 24 bits de mantissa (aproximadamente 7 dígitos decimais de precisão).
- **Cancelamento Catastrófico:** Quando dois números muito próximos são subtraídos, os dígitos mais significativos se cancelam, expondo o ruído de arredondamento nos bits menos significativos:
  $$x = 1.0000001, \quad y = 1.0000000 \implies x - y = 0.0000001$$
  Se esse valor for posteriormente usado como divisor em um filtro IIR ou inversão matricial, os erros propagam-se exponencialmente.

## 2. O Problema da Amostragem Pequena ($N \ll C$) em Covariância
Ao estimar a matriz de covariância espacial $\Sigma \in \mathbb{R}^{C \times C}$ a partir de $N$ amostras:
- Se $N < C$, o posto da matriz $\text{rank}(\Sigma) \le N < C$. A matriz é estritamente singular e não invertível.
- Mesmo quando $N > C$, se $N$ não for pelo menos uma ordem de magnitude maior que $C$, os autovalores menores são sistematicamente subestimados e os maiores superestimados (fenômeno de Marchenko-Pastur).
- O número de condição $\kappa(\Sigma) = \frac{\sigma_{max}}{\sigma_{min}}$ atinge valores astronômicos ($> 10^8$), tornando a solução do sistema linear $w = \Sigma^{-1} (\mu_1 - \mu_2)$ extremamente sensível a flutuações infinitesimais de ruído.

## 3. Regularização de Tikhonov / Diagonal Loading
A estratégia canônica de estabilização numérica consiste em adicionar uma identidade escalonada à matriz de covariância:

$$\Sigma_{reg} = \Sigma + \lambda \cdot I_C$$

Onde:
- $\lambda > 0$ é o parâmetro de regularização (*shrinkage* / carga diagonal).
- $I_C$ é a matriz identidade $C \times C$.

Efeito espectral: se $\Sigma = V \Lambda V^T$ com autovalores $\sigma_i$, então:
$$\Sigma_{reg} = V (\Lambda + \lambda I) V^T$$
Todos os autovalores são deslocados por $+\lambda$. Logo, $\sigma_{min}(\Sigma_{reg}) \ge \lambda > 0$, garantindo que a matriz seja estritamente positiva definida e perfeitamente condicionada para inversão.

## 4. O Que a Próxima Sala Assume
A próxima sala (`nt-cs-harness`) integra esses cuidados matemáticos em baterias automatizadas de testes e detecção de regressão em pipelines neurais.
