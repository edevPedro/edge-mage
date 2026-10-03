# História — O Milagre do Ruído Branco

Na apresentação de encerramento do trimestre em uma aceleradora de tecnologia neural, um jovem cientista de dados subiu ao palco para mostrar os resultados de um pipeline automatizado de aprendizado de máquina para decodificação de intenção motora em sinais de EEG.

"Nosso modelo alcançou noventa e quatro por cento de acurácia em um banco de quarenta ensaios," anunciou ele, exibindo matrizes de confusão quase diagonais. "A técnica foi capaz de selecionar as melhores frequências cerebrais de forma completamente autônoma."

No fundo da plateia, um professor sênior de estatística e neuroengenharia pediu acesso ao repositório de código e abriu a função de pré-processamento. Ele notou que a rotina calculava a correlação de Pearson entre as centenas de variáveis espectrais e os rótulos de classe antes da linha que chamava a divisão de treino e teste.

O professor pediu o teclado, gerou uma matriz de números puramente aleatórios usando uma distribuição normal padrão e atribuiu rótulos de zero e um por sorteio de cara ou coroa. Ele rodou exatamente o mesmo script sobre o ruído puro.

Em segundos, o terminal imprimiu: acurácia no teste de oitenta e oito por cento.

"Você acaba de decodificar o futuro usando ruído térmico aleatório," disse o professor em tom solene. "Isso se chama vazamento de dados ou análise circular. Ao selecionar as variáveis usando a base de dados inteira antes de separar o teste, você permite que flutuações estatísticas do teste contaminem o modelo de treino. O modelo não aprendeu neurofisiologia motora; ele decorou o ruído do teste."

O professor então reescreveu a rotina usando partição contígua em blocos e forçou a seleção de variáveis a acontecer exclusivamente dentro dos folds de treino.

A acurácia sobre o ruído despencou imediatamente para cinquenta por cento — exatamente o nível do acaso.

"A validação cruzada não é um botão para inflar métricas e agradar investidores," concluiu o pesquisador. "É uma barreira de integridade científica. Se o teste vazar para o treino, seu código mente para você."
