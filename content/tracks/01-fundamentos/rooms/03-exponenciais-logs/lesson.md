# Exponenciais e logaritmos

Antes de softmax, cross-entropy e learning rates, precisamos de `exp` e `log` com intuição — não só fórmulas.

## Exponencial

`exp(x) = eˣ` cresce (ou decai) rápido. Propriedades úteis:

- `eᵃ · eᵇ = eᵃ⁺ᵇ`
- `(eᵃ)ᵇ = eᵃᵇ`
- `e⁰ = 1`, `eˣ > 0` para todo x real

Em redes, logits passam por `exp` no softmax. Valores grandes de logit estouram float32 — daí a estabilidade numérica depois.

## Logaritmo

`ln` (log natural) é a inversa de `exp`: `ln(eˣ) = x` e `e^{ln x} = x` (x > 0).

Mudança de base (útil em bits/bytes e informação):

- `log₂(x) = ln(x) / ln(2)`
- `log₁₀(x) = ln(x) / ln(10)`

## Produtos viram somas

`ln(ab) = ln a + ln b` e `ln(aᵇ) = b · ln a`.

Cross-entropy usa `−log p`: quanto menor a probabilidade da classe correta, maior a perda. Isso só faz sentido se `p ∈ (0, 1]` e log for bem definido.

## Ponte Edge AI

- Softmax: `e^{z_i} / Σ e^{z_j}`
- CE: `−log p_k`
- Escalas em dB / SNR em sensores: razões → logs
