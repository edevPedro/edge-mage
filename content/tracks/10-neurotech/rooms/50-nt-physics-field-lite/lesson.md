# Desafio — Razão de Atenuação Geométrica de Campo ($1/r^2$)

## 1. Objetivo do Desafio
Implementar a rotina de cálculo da razão de atenuação geométrica de potencial entre duas distâncias radiais a partir de uma fonte dipolar.

## 2. Especificação Técnica e Formulação
Dadas as distâncias `r_near` e `r_far` em metros a partir do centro da fonte (com $r_{\text{far}} > r_{\text{near}} > 0$):
- Implemente a função `field_decay_ratio(r_near, r_far)`:
  $$\text{ratio} = \left( \frac{r_{\text{far}}}{r_{\text{near}}} \right)^2$$
- Retorne o valor flutuante da razão de atenuação teórica.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que $r_{\text{near}} > 0$.
- Para $r_{\text{near}} = 0.015\text{ m}$ e $r_{\text{far}} = 0.030\text{ m}$ (o dobro da distância), a razão deve ser estritamente $4.0$.
