# Desafio — Cálculo do Tamanho de Efeito ($d$ de Cohen)

## 1. Objetivo do Desafio
Implementar a rotina de cálculo do tamanho de efeito padronizado $d$ de Cohen entre dois grupos amostrais, compreendendo sua independência em relação ao tamanho total da amostra.

## 2. Especificação Técnica e Formulação
Dadas as médias $\mu_1$ e $\mu_2$ e os desvios-padrão amostrais $s_1$ e $s_2$ de dois conjuntos de ensaios independentes:
- Implemente a função `cohens_d(m1, s1, m2, s2)`:
  $$s_{\text{pooled}} = \sqrt{\frac{s_1^2 + s_2^2}{2}}$$
  $$d = \frac{m1 - m2}{s_{\text{pooled}}}$$

## 3. Critérios de Validação e Armadilhas
- Se $s_{\text{pooled}} = 0$, trate a divisão por zero retornando zero ou tratando a igualdade de médias.
- Lembre-se: em projetos de pesquisa sérios, todo relato de acurácia ou modulação de ERD deve vir acompanhado do tamanho de efeito $d$ correspondente.
