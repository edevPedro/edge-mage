# Desafio — Multiplicação Matriz-Vetor e Matriz de Covariância Amostral

## 1. Objetivo do Desafio
Implementar a multiplicação matricial por vetor e o cálculo da matriz de covariância espacial amostral a partir de uma matriz de dados multicanal centralizada.

## 2. Especificação Técnica e Formulação
1. **Multiplicação Matriz-Vetor:** Implemente `matvec(A, x)` onde $A$ é uma matriz $M \times N$ e $x$ é um vetor de comprimento $N$, retornando um vetor $y$ de comprimento $M$:
   $$y_i = \sum_{j=0}^{N-1} A_{i, j} x_j$$
2. **Covariância Amostral:** Implemente `sample_covariance(X)` onde $X$ é uma matriz $C \times T$ com média zero nas linhas, retornando a matriz $\Sigma$ de dimensões $C \times C$:
   $$\Sigma_{i, j} = \frac{1}{T - 1} \sum_{t=0}^{T-1} X_{i, t} X_{j, t}$$

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que a matriz resultante seja perfeitamente simétrica: $\Sigma_{i, j} = \Sigma_{j, i}$.
- Trate o caso de $T \le 1$ levantando `ValueError` por insuficiência de amostras para estimativa não-viesada.
