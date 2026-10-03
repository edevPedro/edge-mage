# História — O Deadline Perdido por Quatro Milissegundos

No laboratório de controle neural em tempo real, um desenvolvedor de visão computacional tentava adaptar uma arquitetura de aprendizado profundo para guiar um cursor na tela através de imagética motora. O modelo alcançava noventa e cinco por cento de acurácia nos arquivos estáticos gravados na semana anterior.

Entretanto, durante os testes ao vivo com o voluntário em malha fechada, o cursor movia-se de maneira engasgada, com atrasos perceptíveis que faziam o usuário errar sistematicamente os alvos visuais.

"O classificador roda perfeitamente no computador com placa gráfica," protestava o programador, exibindo o log de acertos. "O tempo de inferência da rede é de apenas quarenta milissegundos."

A arquiteta de sistemas de tempo real sentou-se na estação de trabalho, conectou um osciloscópio a um pino GPIO da placa de aquisição e colocou um fotodiodo colado na tela do monitor do voluntário para medir o tempo decorrido entre a emissão do sinal cerebral e a atualização física dos pixels na tela.

"Seu modelo de inferência leva quarenta milissegundos," começou ela, desenhando a linha do tempo no quadro. "A taxa de amostragem do amplificador é de duzentos e cinquenta hertz, gerando quatro milissegundos de atraso de ingestão de pacote. O banco de filtros espaciais biquads consome quase um milissegundo. E o monitor de sessenta hertz do sujeito tem uma taxa de varredura que adiciona dezesseis vírgula seis milissegundos puros de espera de sincronização vertical."

Ela somou os três estágios: quatro mais quarenta vírgula oito mais dezesseis vírgula seis. O total resultou em sessenta e um vírgula quatro milissegundos.

"O deadline máximo estipulado pelo protocolo neurofisiológico para sensação de agência motora é de cinquenta milissegundos," apontou a engenheira. "Seu sistema quebra o prazo em mais de onze milissegundos. Pior ainda: como você processa janelas a cada vinte e cinco milissegundos e seu código demora quarenta para rodar, a fila FIFO de entrada enche e descarta amostras a cada três segundos."

O programador olhou para o gráfico de overrun. Substituindo a rede convolucional pesada por um Discriminante Linear de Fisher regularizado, o tempo de cálculo despencou de quarenta para cinco milissegundos. A latência total caiu para vinte e cinco vírgula seis milissegundos, bem abaixo do prazo fatal. O cursor deslizou pela tela com controle imediato e responsivo.
