# História — O Kernel que Enxergava Mais Que a Rede Inteira

O laboratório de neuro mediu uma coisa curiosa: um aluno trocou a camada densa
de 48.000×1.024 por uma convolução 1D de kernel 32 e a acurácia *subiu*.

— Como assim menos parâmetros funciona melhor? — perguntou o colega.

— Porque a camada densa olha para 48.000 pontos como se cada um fosse uma
  coordenada independente. A convolução olha o sinal do jeito que ele é:
  uma janela que se repete no tempo. Os mesmos 32 pesos passam por todas as
  719 posições. Ela não tenta decorar "a amostra 40.112 é importante"; ela
  aprende o formato do transiente.

No quadro, o aluno desenhou a sequência:
1. conv temporal de 32 taps → bank de filtros aprendido;
2. depthwise espacial → um filtro por canal — a topografia do eletrodo;
3. separável 1×1 → mistura as bandas antes do classificador.

— Isso é o EEGNet. Menos de 3.000 parâmetros para 64 canais. E o melhor: cada
  camada sabe o que está fazendo por causa do bias que a física deu a ela.

O professor anotou na margem do código: "share weigths, not hope".