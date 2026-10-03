# História — A Janela Temporal da Intenção Motora

Na bancada de testes eletrofisiológicos, um pesquisador e um desenvolvedor de firmware ajustam o protocolo de calibração baseado no paradigma de Graz. O voluntário na cabine acústica observa uma tela onde uma cruz de fixação aparece no tempo zero. Três segundos depois, uma seta visual aponta para a direita, instruindo o participante a realizar a imagética motora da mão direita por quatro segundos contínuos.

O desenvolvedor executa um script inicial de extração de potência espectral, mas os resultados de acurácia de classificação não passam de 52%. Olhando os gráficos temporais, o pesquisador percebe o equívoco: o algoritmo estava calculando a potência da banda $\mu$ integrando a sessão inteira do experimento, misturando os momentos de repouso, as instruções visuais e a tarefa motora ativa.

— Uma intenção motora voluntária não é um estado estático permanente — explica o pesquisador. — No instante em que o comando visual (cue) aparece, o córtex visual processa a informação e, cerca de 500 milissegundos depois, o córtex sensoriomotor inicia a Dessincronização Relacionada a Evento (ERD). Para decodificar a intenção, precisamos fatiar o sinal temporal com precisão cirúrgica em torno do evento de trigger: isolar uma janela pré-estímulo (baseline) e uma janela pós-estímulo (ação motora).

No eletrodo $C3$, posicionado sobre o hemisfério esquerdo que controla a mão direita contralateral, o fatiamento temporal revela com clareza a queda de mais de 40% na potência das frequências de $8\text{--}12\text{ Hz}$ e $18\text{--}24\text{ Hz}$ exatamente entre 0.5 e 2.5 segundos após o cue.

O desenvolvedor implementa a rotina de fatiamento (`slice_epoch`), definindo os limites relativos de amostras `[trigger - pre, trigger + post)`. Com os ensaios temporais sincronizados com o relógio do experimento, o contraste contralateral/ipsilateral entre $C3$ e $C4$ atinge nitidez cristalina, permitindo que o classificador separe as classes com precisão.
