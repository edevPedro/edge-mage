# Desafio — Extração de Características Multibanda (FBCSP Features)

## 1. Objetivo do Desafio
Implementar a rotina de extração de características multibanda do algoritmo FBCSP, projetando sinais filtrados em múltiplas bandas de frequência através de pesos espaciais dedicados.

## 2. Especificação Técnica e Formulação
Dada uma lista de matrizes de epochs `band_epochs` (onde cada elemento $X_b$ tem dimensões $C \times T$ correspondentes a uma sub-banda) e uma lista de matrizes de filtros espaciais `spatial_weights` (onde cada elemento $W_b$ tem dimensões $K \times C$ com os vetores de filtro nas linhas):
- Implemente a função `fbcsp_features(band_epochs, spatial_weights)`:
  - Para cada sub-banda $b$, projete o sinal: $S_b = W_b X_b$.
  - Calcule a variância de cada linha filtrada e aplique $\log_{10}(\text{Var} + 10^{-10})$.
  - Concatene todas as características das sub-bandas em uma lista unidimensional de floats.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que o número total de características retornadas seja exatamente $\text{número de bandas} \times K$.
- Lembre-se: esta sala é uma matéria eletiva e não bloqueia a progressão obrigatória para o Mago Supremo.
