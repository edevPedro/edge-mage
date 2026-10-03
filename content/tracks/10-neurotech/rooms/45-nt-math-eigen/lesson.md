# Desafio — Iteração de Potência (Power Iteration) para Autovalor Dominante

## 1. Objetivo do Desafio
Implementar o algoritmo clássico de Iteração de Potência para encontrar o maior autovalor e o autovetor dominante correspondente de uma matriz de covariância simétrica $2 \times 2$.

## 2. Especificação Técnica e Formulação
Dada uma matriz simétrica $A \in \mathbb{R}^{2 \times 2}$ e o número de iterações `num_simulations`:
- Implemente a função `power_iteration(A, num_simulations=50)`:
  1. Inicialize $v = [1.0, 1.0]^T / \sqrt{2}$.
  2. A cada iteração: calcule $w = A v$, normalize $v = w / \|w\|_2$.
  3. Calcule o autovalor escalar: $\lambda = v^T A v$.
  4. Retorne a tupla `(eigenvalue, eigenvector)` contendo o autovalor escalar e a lista com as duas componentes do autovetor unitário.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que o autovetor retornado seja unitário ($\|v\|_2 = 1.0$).
- Para a matriz de teste canônica $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$, o autovalor dominante deve convergir exatamente para $\lambda = 3.0$ com autovetor $[1/\sqrt{2}, 1/\sqrt{2}]$.
