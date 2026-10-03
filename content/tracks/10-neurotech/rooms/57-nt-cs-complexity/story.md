# História — A Armadilha do O(C² W)

Na bancada de testes de um sistema de BCI de alta densidade (128 canais a 1000 Hz), a equipe de processamento de sinais comemorava a integração de um novo estimador de covariância espacial adaptativo. Nos testes offline com arquivos gravados no disco NVMe, o script em Python processava 10 minutos de dados em poucos segundos.

Porém, ao ligar o streaming em tempo real na placa embarcada com processador de baixo consumo, o sistema colapsou. A fila de pacotes cresceu descontroladamente, a latência de exibição saltou de 10 milissegundos para mais de dois segundos, e o buffer do driver de aquisição começou a descartar amostras aos milhares.

O engenheiro de sistemas embarcados abriu o profiler de CPU e apontou para o gargalo:

— "Vocês estão recalculando a matriz de covariância completa a cada nova amostra recebida para 128 canais. Qual é a complexidade assintótica dessa operação?"

O cientista de dados hesitou:

— "É uma multiplicação de matrizes... $X X^T$ para uma janela de $W$ amostras..."

— "Exatamente: $\mathcal{O}(C^2 W)$", sentenciou o engenheiro. "Com 128 canais e uma janela de 500 amostras, são mais de oito milhões de operações de ponto flutuante por amostra. A mil amostras por segundo, vocês precisam de 8 GFLOPS sustentados apenas para a covariância ingênua, sem contar a inversão $\mathcal{O}(C^3)$ para o filtro de clareamento (whitening). Nosso microprocessador embarcado simplesmente não tem essa largura de banda de memória."

O engenheiro puxou o diagrama de arquitetura:

— "Em neuroengenharia de tempo real, algoritmos elegantes que violam o orçamento de latência (*latency budget*) são inúteis. Ou vocês reduzem o número de canais $C$, ou usam atualizações recursivas de posto-1 $\mathcal{O}(C^2)$, ou processam em blocos (*hops*). Todo pipeline online começa com uma checagem rigorosa de budget temporal: se o tempo de processamento estimado ultrapassar o deadline de entrega, o loop online atrasa, o buffer estoura e o BCI falha."
