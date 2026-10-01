# Loss & Learning Rate

A **loss** mede o erro do modelo. Treinar = ajustar parâmetros para reduzir a loss (em média no dataset).

## MSE

Para regressão: `MSE = média (ŷ − y)²`. Erros ±1 contam igual após o quadrado.

## Classificação

Mais adiante: cross-entropy com softmax. A intuição é a mesma — escalar (ou soma) que queremos minimizar.

## Learning rate

η controla o tamanho do passo. Agenda comum: começar maior e decair (cosine decay, step decay).

Demasiado grande → loss sobe/oscila. Demasiado pequeno → treino glacial.

## Treino vs inferência

- **Treino**: forward + backward + update (caro)
- **Inferência**: só forward (o que o edge prioriza)
