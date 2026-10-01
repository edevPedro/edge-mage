# Probabilidade mínima para ML

Softmax devolve uma **distribuição de probabilidade** sobre classes. Sem isso, cross-entropy não tem interpretação.

## Axiomas úteis

Para eventos discretos com probabilidades `p_i`:

- `p_i ≥ 0`
- `Σ p_i = 1` (espaço completo)

Um vetor que obedece isso é uma distribuição categórica — exatamente o que o softmax produz.

## Independência e esperança (intuição)

- Se A e B são independentes, `P(A∩B) = P(A)P(B)`.
- Esperança de uma VA discreta: `E[X] = Σ x_i p_i`.

Em classificação, a cross-entropy é a surpresa média de prever p quando a verdade é y (one-hot).

## Log-probabilidade

`log p` (p ∈ (0,1]) é negativo ou zero. Multiplicar probabilidades independentes vira **somar** log-probs — numericamente mais estável e a base de muitas losses.

## Ligação com o próximo quarto

Softmax garante `p_i > 0` e `Σ p = 1`. CE pune `−log p_correta`: se o modelo atribui pouca massa à classe certa, a loss explode.
