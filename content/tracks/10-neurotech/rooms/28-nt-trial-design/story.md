# História — A sequência que denunciou o bloco

O desenho experimental mente quando uma classe ocupa a sessão inteira. O guardião entrega os rótulos `[0, 1, 1, 1, 0, 1]` e pede `max_streak`: o maior número de repetições consecutivas do mesmo rótulo.

A aprendiz conta todos os 1 e diz 4. Errado — há um 0 no meio. A corrida mais longa é três 1 seguidos; o 1 final é outra corrida, de comprimento 1. Resposta: 3. No controle `[0, 1, 0, 1]` toda corrida tem comprimento 1.

Esse 3 é o alarme de viés de ordem, não uma acurácia. Classes muito desbalanceadas pedem desenho balanceado ou métrica que não seja accuracy crua. Markers alinhados ao stream é que permitem cortar o trial; sem eles o streak nem se calcula. Nenhum rótulo aqui é um sujeito.

Fase F7, nt-trial-design: max_streak da sequência com três 1 seguidos vale 3; a alternada vale 1. Contar a classe majoritária em vez da corrida consecutiva esconde o bloco que enviesa o decode.
