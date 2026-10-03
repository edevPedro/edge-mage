# História — A Fraude Involuntária dos 99%

A sala de reuniões estava em euforia. Uma equipe recém-formada de ciência de dados apresentava os resultados de um modelo de aprendizado profundo aplicado a um conjunto de dados de eletroencefalografia motora:

— "Alcançamos 99,4% de acurácia na decodificação de intenção de movimento. Nosso modelo supera todos os trabalhos publicados na literatura internacional!"

O engenheiro de confiabilidade e QA (Quality Assurance) olhou para os gráficos com ceticismo profissional:

— "Com sinais de EEG de escalpo e relação sinal-ruído de $-10\text{ dB}$? Isso não é avanço científico; é vazamento de dados (*data leakage*) ou falha no harness de testes."

Ele pediu para inspecionar o código de avaliação. Não demorou cinco minutos para encontrar os problemas:

— "Vejam aqui: primeiro, vocês não fixaram a semente do gerador de números pseudoaleatórios (`seed`). Cada execução gerava um resultado estocástico diferente. Segundo, vocês normalizaram o dataset inteiro antes de fazer a divisão de treino e teste. Terceiro, o stream serial perdeu pacotes durante a aquisição, e em vez de detectar a descontinuidade temporal nos números de sequência, o código simplesmente concatenou os blocos como se o tempo fosse contínuo."

O engenheiro abriu o terminal e iniciou a construção de um harness automatizado:

— "Em engenharia séria, nós não confiamos em 'prints' no console ou demonstrações manuais. Nós construímos *test harnesses* determinísticos com sementes fixas, asserções matemáticas rigorosas e detectores automáticos de anomalias no fluxo de dados. Se um pacote serial com contador de sequência saltar de 5 para 8, seu pipeline precisa acusar imediatamente que 2 pacotes foram perdidos. Se um teste falhar após uma alteração no código, isso é uma regressão que impede o deploy. Sem um harness confiável, sua pesquisa é apenas ilusão estocástica."
