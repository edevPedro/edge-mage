# Desafio — Razão de Dessincronização do Paradigma Berlin BCI

## 1. Objetivo do Desafio
Implementar a regra de decisão de classificação de imagética motora lateralizada inspirada no paradigma clássico do Berlin BCI, calculando a razão de potência entre os eletrodos sensoriomotores contralaterais $C3$ e $C4$.

## 2. Especificação Técnica
Implemente a função `berlin_erd_ratio(c3_mu, c4_mu)`:
- Calcule a razão de potência espectral:
  $$\text{ratio} = \frac{c3\_mu}{c4\_mu}$$
- Determine a classe predita com base na dominância hemisférica contralateral:
  - Se $\text{ratio} < 1.0$: o canal $C3$ sofreu maior atenuação (dessincronização no hemisfério esquerdo), indicando imagética da **mão direita** (`'right_hand'`).
  - Se $\text{ratio} \ge 1.0$: o canal $C4$ sofreu maior ou igual atenuação, indicando imagética da **mão esquerda** (`'left_hand'`).
- Retorne a tupla `(ratio, prediction)`.

## 3. Exemplos Canônicos de Validação
```python
# C3 atenuado (5.0) contra C4 alto (20.0): ratio = 0.25 -> right_hand
ratio, pred = berlin_erd_ratio(5.0, 20.0)
assert ratio == 0.25 and pred == "right_hand"

# C4 atenuado (10.0) contra C3 alto (25.0): ratio = 2.5 -> left_hand
ratio2, pred2 = berlin_erd_ratio(25.0, 10.0)
assert ratio2 == 2.5 and pred2 == "left_hand"
```

## 4. Critérios de Validação e Armadilhas
- Certifique-se de retornar as strings exatamente como `'right_hand'` e `'left_hand'` em minúsculas com sublinhado.
