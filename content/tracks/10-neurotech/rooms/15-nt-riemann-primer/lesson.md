# Desafio — Distância Riemanniana em Matrizes Diagonais

## 1. Objetivo do Desafio
Compreender a natureza não-euclidiana do espaço de covariâncias e implementar o cálculo da distância geodésica Riemanniana AIRM restrita a matrizes diagonais estritamente positivas.

## 2. Especificação Técnica e Formulação
Dadas duas listas ou vetores diagonais de variâncias estritamente positivas $d_1 = [a_0, a_1, \dots, a_{C-1}]$ e $d_2 = [b_0, b_1, \dots, b_{C-1}]$:
- Implemente a função `riemann_diag_dist(d1, d2)` calculando a métrica:
  $$\text{dist}(d_1, d_2) = \sqrt{\sum_{i=0}^{C-1} \left(\ln\left(\frac{a_i}{b_i}\right)\right)^2}$$

## 3. Critérios de Validação e Armadilhas
- Certifique-se de utilizar o logaritmo natural (`math.log`).
- Verifique que se $d_1 = d_2$, a distância resultante deve ser estritamente zero ($0.0$).
- Lembre-se: em matrizes reais, todas as variâncias devem ser estritamente positivas ($a_i > 0, b_i > 0$).
