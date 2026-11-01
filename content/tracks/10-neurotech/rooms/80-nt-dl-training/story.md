# História — 29 Épocas de Autoconfiança

Um pós-graduando treinou uma rede própria (2 camadas, 256 neurônios) durante
uma madrugada. Às 4h da manhã a loss de treino chegou a 0,001. Ele foi dormir
satisfeito. Na reunião da tarde, apresentou o gráfico: 99,1% de acurácia.

A orientadora esperou ele terminar e perguntou:
— E na validação?
— ...na validação, 54%. Mas o treino está *realmente* baixo.
— Isso não é notícia. Isso é memorização. Com 120 trials e uma rede de 200 mil
  pesos, cada trial tem 1.600 parâmetros pra decorar. Sua CE no treino só te
  diz uma coisa: que a sua rede anotou *as respostas*. Tune no validation,
  aplique weight decay e dropout, e *pare* quando a validação degradar — não
  quando o treino zerar.

Ele rodou de novo com regularização + early stop. Treino: 91%. Validação: 78%.
κ = 0,56. Ninguém aplaudiu a queda no treino.

— Agora sim — disse ela. — Baixou o treino e subiu a verdade. É assim que se
  treina em dados neurais: a perda de treino é o seu relógio; a validação é o
  seu contrato.