# Lição — Autovalores e Power Iteration

## 1. Contexto Operacional
O método das potências (power iteration) é um algoritmo numérico fundamental em sistemas de computação em tempo real. Ele extrai de forma rápida e iterativa o autovetor associado ao maior autovalor de uma matriz simétrica, sem exigir decomposições matriciais pesadas.

## 2. Passo a Passo Matemático

### Power Iteration em Matriz 2x2
Dada uma matriz simétrica $A \in \mathbb{R}^{2 \times 2}$ e número de iterações $K$:
1. Inicialize $v = [1.0, 1.0]^T$.
2. Para cada iteração:
   - Calcule $w = A v$:
     $$w_0 = A_{00} v_0 + A_{01} v_1, \quad w_1 = A_{10} v_0 + A_{11} v_1$$
   - Calcule a norma $\text{norm} = \sqrt{w_0^2 + w_1^2}$.
   - Atualize $v = [w_0 / \text{norm}, w_1 / \text{norm}]$.
3. Retorne o autovetor $v$.

### Componente Principal 2x2 (Quociente de Rayleigh)
Dada a matriz de covariância `cov`:
1. Execute `v = power_iteration(cov, num_iters=25)`.
2. Calcule o autovalor associado através do quociente de Rayleigh:
   $$\lambda = v^T \text{cov} \, v = v_0 (\text{cov}_{00} v_0 + \text{cov}_{01} v_1) + v_1 (\text{cov}_{10} v_0 + \text{cov}_{11} v_1)$$
3. Retorne a tupla `(v, lambda)`.

Consulte [NumPy linalg eig](https://numpy.org/doc/stable/reference/generated/numpy.linalg.eig.html) para validar resultados de autovalores.
