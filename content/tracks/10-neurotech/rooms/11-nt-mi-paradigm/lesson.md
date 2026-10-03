# Desafio — Fatiamento Temporal de Ensaios (Epoch Slicing)

## 1. Objetivo do Desafio
Implementar a rotina fundamental de fatiamento temporal de epochs a partir de uma série contínua de amostras e um índice de trigger, garantindo que as janelas pré e pós-evento preservem a integridade de índices para a análise de ERD/ERS.

## 2. Especificação Técnica e Formulação
Dado um array unidimensional ou lista de amostras `signal`, um índice inteiro `trigger`, e as durações `pre` e `post` em número de amostras:
- Implemente a função `slice_epoch(signal, trigger, pre, post)` que retorna o sub-array correspondente ao intervalo semiaberto:
  $$\text{resultado} = \text{signal}[\text{trigger} - \text{pre} : \text{trigger} + \text{post}]$$
- O comprimento retornado deve ser exatamente $\text{pre} + \text{post}$ amostras.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de respeitar o indexamento zero da linguagem.
- Em pipelines reais de produção, verifique sempre se $\text{trigger} - \text{pre} \ge 0$ e $\text{trigger} + \text{post} \le \text{len}(\text{signal})$ para evitar exceções de limites de buffer (IndexError).
