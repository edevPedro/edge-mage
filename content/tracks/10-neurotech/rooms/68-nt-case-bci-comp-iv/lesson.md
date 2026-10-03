# Desafio — Cálculo da Matriz de Confusão Binária

## 1. Objetivo do Desafio
Implementar a rotina de avaliação de desempenho de classificadores binários através da contagem determinística dos elementos da matriz de confusão: Verdadeiros Positivos (TP), Falsos Positivos (FP), Verdadeiros Negativos (TN) e Falsos Negativos (FN).

## 2. Especificação Técnica
Implemente a função `calc_confusion(y_true, y_pred)`:
- Receba duas listas ou iteráveis de mesmo comprimento contendo rótulos binários discretos ($0$ ou $1$): `y_true` (valores reais) e `y_pred` (predições do modelo).
- Inicialize contadores inteiros para `tp`, `fp`, `tn`, `fn` em zero.
- Para cada par $(y_t, y_p)$ correspondente:
  - Se $y_t == 1$ e $y_p == 1$: incremente `tp`.
  - Se $y_t == 1$ e $y_p == 0$: incremente `fn`.
  - Se $y_t == 0$ e $y_p == 1$: incremente `fp`.
  - Se $y_t == 0$ e $y_p == 0$: incremente `tn`.
- Retorne um dicionário Python com a estrutura exata:
  `{'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}`

## 3. Exemplo de Referência
```python
y_true = [1, 1, 0, 0]
y_pred = [1, 0, 0, 1]
cm = calc_confusion(y_true, y_pred)
# Par 1: (1, 1) -> tp = 1
# Par 2: (1, 0) -> fn = 1
# Par 3: (0, 0) -> tn = 1
# Par 4: (0, 1) -> fp = 1
assert cm['tp'] == 1 and cm['fn'] == 1 and cm['tn'] == 1 and cm['fp'] == 1
```

## 4. Critérios de Validação e Armadilhas
- Certifique-se de que todas as 4 chaves estejam presentes no dicionário retornado (`'tp'`, `'fp'`, `'tn'`, `'fn'`).
