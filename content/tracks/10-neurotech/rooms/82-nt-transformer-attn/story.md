# História — A Reunião em Que Todos Olharam para Todos

Era uma reunião de design do time de modelos de linguagem. Cada pessoa
representava um token de uma frase: "o", "gato", "sentou", "no", "tapete".

O problema: traduzir "The cat sat on the mat" para português. Uma RNN leria
um por um, da esquerda para a direita, guardando um estado compresso. O
apresentador apagou o quadro e desenhou uma matriz quadrada 5×5.

— Não precisa dar um "resumo" do contexto. Cada token pergunta ao contexto
  diretamente: "quem de vocês importa para eu decidir meu próximo passo?"
  O "sat" pergunta "quem é o sujeito?" → o "cat" responde alto. O "mat"
  pergunta "onde?" → "on" e "the" respondem. Cada par ganha um peso, e cada
  token devolve uma *soma ponderada* dos conteúdos. Todo mundo olha todo mundo,
  em paralelo, com uma passada de matriz.

O engenheiro de inferência, no fundo da sala, fez a conta:
— E n×n passa a ser o custo: 2.048 tokens de contexto é uma matriz de 4 milhões.
  Dobrou o contexto, esse custo quadruplica.

— Exato. E é essa matriz que vira o working set do kv-cache amanhã. Atenção é
  o cérebro do modelo; o custo O(L²) é a conta que esse cérebro manda para o
  orçamento de inferência.

Todos concordaram sem levantar a mão — figurativo e literalmente ao mesmo tempo.