# História — A Fila que Não Podia Alocar

No laboratório de instrumentação de BCI, a equipe estava testando um driver em Python para capturar pacotes de 8 canais de EEG vindos via porta serial a 250 Hz. Nos primeiros trinta segundos, o streaming funcionava perfeitamente. De repente, a cada dez segundos, o sistema engasgava por 80 milissegundos, perdendo dezenas de amostras consecutivas.

O desenvolvedor de firmware conectou um analisador lógico e chamou o programador de software:

— "Sua aplicação está pausando a thread de leitura serial. O que está acontecendo no seu código a cada dez segundos?"

O programador abriu o editor:

— "Eu criei uma lista dinâmica simples: `buffer.append(sample)`. Quando o tamanho da janela atinge o limite, eu faço `buffer.pop(0)` para remover o mais antigo."

O engenheiro de firmware respirou fundo:

— "Em ciência da computação de sistemas em tempo real, `pop(0)` em uma lista encadeada ou array dinâmico é uma das piores operações possíveis: ela tem complexidade $\mathcal{O}(N)$, exigindo que todos os elementos subsequentes sejam copiados na memória. Pior ainda: o interpretador aloca e desaloca blocos de memória dinamicamente no heap, forçando o coletor de lixo (*garbage collector*) a congelar a execução para limpar os objetos órfãos. É esse congelamento que estoura o buffer serial do chip."

O engenheiro puxou um bloco de notas e desenhou um círculo com ponteiros:

— "Para biosinais de streaming, você nunca aloca memória no caminho crítico. Você pré-aloca um array de capacidade fixa e utiliza aritmética modular de ponteiros de leitura e escrita: um *ring buffer* (buffer circular). Quando novos dados chegam e o buffer está cheio, a política padrão de biopotenciais é o descarte do dado mais antigo (*overwrite*), mantendo sempre os dados mais recentes acessíveis em $\mathcal{O}(1)$ sem nenhuma alocação de memória."
