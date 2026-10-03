# História — O Falso Triunfo dos Vinte Trials

Em uma reunião de sprint de um projeto de BCI experimental para soletração motora, um desenvolvedor júnior apresenta orgulhoso os resultados do decodificador recém-treinado. O relatório exibe um gráfico de barras com 65% de acurácia no teste de validação.

O desenvolvedor argumenta: "O baseline de duas classes é 50%. Com 65%, superamos o acaso por quinze pontos percentuais. Podemos avançar para o teste em malha fechada."

O engenheiro de pesquisa e estatística da equipe pede os logs brutos da sessão. O teste consistiu em apenas 20 trials gravados durante a tarde. O engenheiro abre o quadro e calcula a probabilidade acumulada sob a hipótese nula de que o classificador estava apenas chutando cara ou coroa. Pela distribuição binomial com $N=20$ e $p=0.5$, a probabilidade de acertar 13 ou mais tentativas ao acaso é superior a $13\%$ ($p > 0.05$).

O desenvolvedor é confrontado com a realidade dos números: para um conjunto de 20 trials, a barreira mínima de significância estatística ($\alpha = 0.05$) exige no mínimo 14 acertos (70%). Um resultado de 65% é perfeitamente compatível com o acaso puro. O time rejeita o avanço até que o código implemente a checagem analítica do limiar de chance para qualquer tamanho amostral $N$.
