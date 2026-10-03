# Desafio — Verificação de Orçamento de Latência (Latency Budget)

## 1. Objetivo do Desafio
Implementar uma função de validação de orçamento temporal para verificar se o custo computacional estimado de uma etapa de processamento por amostra cabe dentro do prazo máximo estipulado (*deadline*).

## 2. Especificação Técnica
Implemente a função `within_deadline(n_channels, n_samples, us_per_sample=0.5, deadline_us=1000.0)`:
- Calcule o tempo total estimado de processamento em microssegundos:
  $$t_{proc} = n_{channels} \times n_{samples} \times \text{us\_per\_sample}$$
- Retorne um booleano:
  - `True`: se $t_{proc} \le deadline_{us}$.
  - `False`: se $t_{proc} > deadline_{us}$.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que a comparação seja menor ou igual ($\le$).
- Compreenda que em processamento de tempo real, qualquer estouro de prazo implica perda de determinismo temporal do loop de controle.
