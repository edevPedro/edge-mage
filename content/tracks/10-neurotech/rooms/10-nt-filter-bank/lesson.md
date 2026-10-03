# Desafio — Decomposição Espectral e Máscara de Bandas

## 1. Objetivo do Desafio
Compreender o papel dos bancos de filtros na isolação de ritmos sensoriomotores, dominar o critério de Nyquist para frequências máximas e implementar a função de mascaramento booleano de frequências.

## 2. Especificação Técnica e Formulação
Considere um vetor de frequências de interesse $F = [f_1, f_2, \dots, f_m]$:
- Desenvolva a função `band_mask(freqs, lo, hi)` que recebe uma lista de frequências e retorna uma lista booleana com o mesmo comprimento, contendo `True` se $lo \le f < hi$ e `False` caso contrário:
  $$\text{mask}[i] = (lo \le freqs[i] < hi)$$

## 3. Critérios de Validação e Armadilhas
- Atenção ao intervalo semiaberto: o limite inferior $lo$ é inclusivo, e o limite superior $hi$ é exclusivo.
- Verifique que frequências fora dos limites de Nyquist ($f > f_s / 2$) não sejam consideradas válidas em projetos de filtros.
