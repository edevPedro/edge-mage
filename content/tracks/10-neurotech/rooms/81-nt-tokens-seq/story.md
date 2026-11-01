# História — Como Uma Sigla Virou 30 Mil Pedaços

Na introdução de um curso de modelos de linguagem, a professora perguntou à
turma:
— Quantas palavras existem na língua inglesa?
Respostas: "170 mil", "1 milhão", "infinitas, linguiças novas nascem todo dia".

— Se o meu vocabulário fosse só palavras, toda palavra nova fora da lista viraria
  um token desconhecido — e o modelo teria um plano B tão útil quanto adivinhar.
  Então a gente quebra em subwords. "never" existe e vira "never"; "neverland"
  vira "never" + "##land"; uma palavra fora do dicionário vira uma recombinação
  de pedaços que o modelo já conhece. Um vocabulário de 30 mil pedaços cobre
  quase qualquer input, ao custo de tokens mais longos — que custam memória na
  prefill e latência na geração.

Um aluno de BCI ergueu a mão:
— Isso não é parecido com as minhas janelas? Eu escolho quanto sinal entra por
  trial, e tenho que empacotar tudo num formato fixo pro tensor.
— Exato. Por isso vamos estudar padding, truncation e o custo de cada token:
  no fim, tudo vira uma sequência de números que o modelo precisa caber.

Na sala seguinte, o mesmo aluno proclamava: "cada token é um trial do mundo
das palavras."