# Conceito — Exp e Log

## Exponencial
`exp(x) = e^x` cresce (ou decai) multiplicativamente.

## Logaritmo
`log` é a inversa: `log(exp(x)) = x`.
Propriedades:
- `log(ab) = log a + log b`
- `log(a^k) = k log a`

## Por que importa em ML
Softmax estável, cross-entropy e likelihoods usam `log-sum-exp` para evitar overflow.
