# Desafio — Gerador de Coordenadas de Janelas Deslizantes

## 1. Objetivo do Desafio
Implementar a rotina geométrica de geração de coordenadas de janelas deslizantes (início e fim) para o particionamento determinístico de fluxos contínuos de dados neurais.

## 2. Especificação Técnica e Formulação
Dado um número total de amostras disponíveis `total_len`, o comprimento fixo de cada janela `win_len`, e o deslocamento de passo `step_len`:
- Implemente a função `sliding_windows(total_len, win_len, step_len)` que retorna uma lista de tuplas `(start, end)`:
  $$\text{start}_k = k \times \text{step\_len}, \quad \text{end}_k = \text{start}_k + \text{win\_len}$$
  para todo $k \ge 0$ tal que $\text{end}_k \le \text{total\_len}$.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que nenhuma janela ultrapasse o comprimento total `total_len` ($end \le \text{total\_len}$).
- Se `total_len < win_len`, a função deve retornar uma lista vazia `[]`, indicando que o buffer ainda não possui amostras suficientes para a primeira predição.
