# Lição — Estimação Amostral e Auditoria de Viés

## 1. Contexto Operacional
Estimar parâmetros estatísticos a partir de séries temporais neurais exige precisão sobre os graus de liberdade da amostra. Quando calculamos a variância amostral ou a matriz de covariância espacial em conjuntos de dados com poucas observações, o divisor $N-1$ é indispensável para evitar subestimação sistemática da dispersão.

## 2. Passo a Passo Matemático

### Matriz de Covariância Amostral Multidimensional
Dadas $N$ amostras $X \in \mathbb{R}^{N \times d}$:
1. Calcule o vetor de médias $\mu \in \mathbb{R}^d$: $\mu_j = \frac{1}{N}\sum_{i=1}^N X_{i, j}$.
2. Calcule a matriz de covariância $d \times d$ usando o divisor $N - 1$:
   $$C_{j, k} = \frac{1}{N - 1} \sum_{i=1}^N (X_{i, j} - \mu_j)(X_{i, k} - \mu_k)$$

### Auditoria de Viés na Variância 1D
Dado um vetor de valores $x$ de comprimento $N$:
1. Se $N < 2$, levante `ValueError`.
2. Média: $\bar{x} = \frac{1}{N}\sum x_i$.
3. Variância enviesada (MLE): $S^2_{\text{biased}} = \frac{1}{N} \sum (x_i - \bar{x})^2$.
4. Variância não enviesada: $S^2_{\text{unbiased}} = \frac{1}{N - 1} \sum (x_i - \bar{x})^2$.
5. Razão de viés: $\text{bias\_factor} = \frac{N - 1}{N}$.
6. Retorne `(s2_biased, s2_unbiased, bias_factor)`.

Consulte [Combrisson & Jerbi (2015)](https://doi.org/10.1016/j.jneumeth.2015.03.034) para diretrizes de poder estatístico em estudos de neurociência.
