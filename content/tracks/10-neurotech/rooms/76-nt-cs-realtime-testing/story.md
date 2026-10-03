# História — O Mistério dos Comandos Fantasmas

Em uma exibição pública de uma cadeira de rodas motorizada controlada por imagética motora em tempo real, a equipe de engenharia enfrentava uma situação desconcertante. Nos relatórios médios de telemetria, o pipeline parecia operar com folga: a taxa de amostragem era de 250 Hz (intervalo alvo de 4 milissegundos entre amostras) e o tempo médio de execução do classificador era de apenas 2,1 milissegundos.

No entanto, o usuário da cadeira relatava uma sensação constante de travamento e perda de controle:

— "De vez em quando, a cadeira não responde ao comando no momento certo, e um segundo depois ela dá dois solavancos seguidos."

O engenheiro de sistemas de tempo real conectou uma sonda de rastreamento de timestamps na saída da thread de inferência:

— "Médias escondem os piores casos. Em sistemas de tempo real críticos, a métrica que importa não é o tempo médio, mas o pior caso de execução (*Worst-Case Execution Time* - WCET) e a dispersão temporal (*jitter*)."

Ele colocou o histograma na tela:

— "Vejam: 99% das amostras chegam com intervalos perfeitos de 4 milissegundos. Mas, exatamente a cada 100 amostras, a thread gráfica da interface do usuário trava o processador para redesenhar o espectrograma na tela. O intervalo entre duas amostras consecutivas salta subitamente para 14 milissegundos! Isso é um jitter absurdo de 10 milissegundos contra um alvo de 4."

O engenheiro virou-se para a equipe:

— "Enquanto a thread gráfica bloqueia a CPU, o buffer de entrada do ADC sofre quase um *underrun*, e quando o processador é liberado, duas inferências são processadas em rajada sem respeitar a dinâmica biológica do cérebro. Para certificar um sistema em tempo real, nós precisamos medir o jitter médio real de cada intervalo temporal e contar exatamente quantas vezes a tolerância máxima foi violada. Esse é o teste que separa um brinquedo acadêmico de um dispositivo real."
