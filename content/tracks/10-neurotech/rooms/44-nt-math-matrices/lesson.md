# Lição — Matrizes, Transformações Lineares e Covariância

## 1. Contexto Operacional
Uma matriz em BCI pode representar operadores espaciais (filtros de montagem, redes de ganho do AFE) ou descritores estatísticos de dispersão temporal. No algoritmo de Classificação por Geometria Riemanniana (MDM) e no Common Spatial Patterns (CSP), o objeto primário de análise não é a série temporal bruta, mas a matriz de covariância espacial calculada em cada trial.

## 2. Passo a Passo Matemático

### Transformação Linear $y = Ax$
Para uma matriz $A$ de dimensões $M \times N$ e um vetor $x$ de dimensão $N$:
$$y_i = \sum_{j=0}^{N-1} A_{i, j} x_j$$

### Matriz de Covariância Multicanal 2x2
Dadas $T$ amostras temporais de dois canais, `trials = [[ch1_0, ch2_0], [ch1_1, ch2_1], ...]`:
1. Valide se $T \ge 2$. Se $T < 2$, levante `ValueError`.
2. Calcule a média temporal de cada canal:
   $$\mu_1 = \frac{1}{T} \sum_{t=0}^{T-1} \text{trials}[t][0], \quad \mu_2 = \frac{1}{T} \sum_{t=0}^{T-1} \text{trials}[t][1]$$
3. Calcule as amostras centradas:
   $$\tilde{x}_{t, 0} = \text{trials}[t][0] - \mu_1, \quad \tilde{x}_{t, 1} = \text{trials}[t][1] - \mu_2$$
4. Calcule os elementos da matriz $2 \times 2$ usando o divisor não enviesado $(T - 1)$:
   $$\Sigma_{00} = \frac{1}{T-1} \sum \tilde{x}_{t, 0}^2, \quad \Sigma_{01} = \Sigma_{10} = \frac{1}{T-1} \sum \tilde{x}_{t, 0} \tilde{x}_{t, 1}, \quad \Sigma_{11} = \frac{1}{T-1} \sum \tilde{x}_{t, 1}^2$$
5. Retorne a matriz `[[Σ00, Σ01], [Σ10, Σ11]]`.

Consulte [NumPy matmul](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html) para manipulação de álgebra matricial.
