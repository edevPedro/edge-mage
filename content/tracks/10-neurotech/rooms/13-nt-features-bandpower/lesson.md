# Desafio — Cálculo da Potência Média de Banda (Bandpower)

## 1. Objetivo do Desafio
Implementar a rotina de cálculo da potência média de banda espectral para uma janela discreta de amostras filtradas de EEG, compreendendo sua equivalência com a variância de um sinal com média zero.

## 2. Especificação Técnica e Formulação
Dado um array ou lista de amostras discretas $X = [x_0, x_1, \dots, x_{N-1}]$ correspondentes a um sinal filtrado na banda de interesse:
- Implemente a função `bandpower(xs)` que retorna a média da soma dos quadrados das amostras:
  $$\text{bandpower}(X) = \frac{1}{N} \sum_{i=0}^{N-1} x_i^2$$

## 3. Critérios de Validação e Armadilhas
- Certifique-se de tratar a divisão pelo número de amostras $N = \text{len}(xs)$. Se o array estiver vazio, a função deve levantar exceção ou retornar zero conforme o contrato.
- A potência de banda é estritamente não-negativa ($P \ge 0$). Qualquer valor negativo indica erro de sinal na implementação.
