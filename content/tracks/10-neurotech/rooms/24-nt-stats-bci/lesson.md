# Desafio — Teste de Permutação Não-Paramétrico

## 1. Objetivo do Desafio
Implementar a rotina de teste de permutação monte-carlo para estimar o valor-p empírico da diferença entre duas distribuições de scores de BCI, sem assumir normalidade gaussiana.

## 2. Especificação Técnica e Formulação
Dadas duas listas de scores de acurácia $A$ e $B$, e o número de repetições `n_permutations`:
- Implemente `permutation_p_value(scores_a, scores_b, n_permutations)`:
  1. Calcule a diferença média observada: $D_{\text{obs}} = \text{mean}(A) - \text{mean}(B)$.
  2. Concatene $A$ e $B$ em um array conjunto.
  3. Para cada permutação: embaralhe o array conjunto aleatoriamente, divida nos tamanhos originais $N_A$ e $N_B$, e calcule a diferença simulada $D_i = \text{mean}(A_i) - \text{mean}(B_i)$.
  4. Retorne a proporção de permutações em que a diferença simulada foi maior ou igual à diferença observada:
     $$p = \frac{\sum_{i=1}^P \mathbb{I}(D_i \ge D_{\text{obs}})}{P}$$

## 3. Critérios de Validação e Armadilhas
- Utilize gerador pseudoaleatório com determinismo quando fixada a semente.
- Se a diferença observada for negativa, o teste unilateral à direita deve refletir a proporção correspondente.
