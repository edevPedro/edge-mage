# Desafio — Média de Periodogramas pelo Método de Welch

## 1. Objetivo do Desafio
Implementar a rotina de agregação e média espectral do método de Welch sobre segmentos temporais pré-janelados, reduzindo a variância da densidade espectral de potência (PSD).

## 2. Especificação Técnica e Formulação
Dada uma matriz ou lista de listas `segments`, onde cada linha contém o espectro de potência estimado de um segmento individual de EEG com $B$ bins de frequência:
- Implemente a função `welch_average_psd(segments)`:
  $$S_{\text{avg}}[j] = \frac{1}{K} \sum_{k=0}^{K-1} \text{segments}[k][j]$$
  para cada bin de frequência $j = 0, \dots, B-1$.
- A função deve retornar uma lista com $B$ valores flutuantes contendo a densidade espectral média.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que todos os segmentos possuam rigorosamente o mesmo número de bins de frequência $B$.
- Se a lista de segmentos estiver vazia, retorne lista vazia `[]`.
