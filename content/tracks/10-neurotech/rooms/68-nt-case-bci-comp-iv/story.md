# História — A Ilusão do Leaderboard

Em um fórum online de competições de ciência de dados, um participante publicou um repositório no GitHub com o título triunfante: *"Superei o estado da arte da BCI Competition IV com 99,8% de acurácia no Graz Dataset 2a!"*

Na seção de comentários, os organizadores originais da competição de 2012 (Tangermann et al.) e pesquisadores de EEG postaram uma série de perguntas técnicas:

— "Qual foi o seu protocolo de validação cruzada? Como você evitou vazamento de informação entre blocos temporais contíguos? E, mais importante: qual foi o seu coeficiente Kappa de Cohen ($\kappa$) oficial?"

O autor do repositório admitiu timidamente:

— "Eu juntei todos os arquivos `.gdf`, embaralhei aleatoriamente todas as épocas com `train_test_split(shuffle=True)` e usei acurácia simples como métrica única."

O pesquisador sênior pegou o caso para uma aula prática com sua equipe:

— "Vejam este exemplo de como não fazer ciência. Em interfaces cérebro-computador e na BCI Competition IV, nós lidamos com séries temporais de sessões contínuas. Se você embaralha épocas vizinhas, seu modelo decodifica a impedância transitória do eletrodo e a respiração lenta do voluntário, não a intenção motora."

Ele abriu a tabela de validação:

— "Além disso, a métrica oficial de competições de BCI nunca é acurácia crua sem contexto; é o coeficiente Kappa ou a matriz de confusão completa. A matriz de confusão quantifica exatamente onde o modelo acerta e erra: Verdadeiros Positivos (TP), Falsos Positivos (FP), Verdadeiros Negativos (TN) e Falsos Negativos (FN). Emular um benchmark consagrado é um exercício fundamental de humildade técnica: serve para testar sua disciplina metodológica, e não para reivindicar falsas vitórias sobre líderes históricos."
