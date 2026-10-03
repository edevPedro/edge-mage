# História — Meia volta não é volta inteira

A ISR não processa a janela. O DMA escreve, e `check_dma_irq(write, prev, half, full)` só diz se cruzou metade ou o fim. Buffer de 1024, metade em 512.

Primeiro par: ponteiro anterior 500, agora 520. Cruzou 512, não cruzou o wrap. HT verdadeiro, TC falso. Quem marca os dois porque “passou de 512” acorda a tarefa errada.

Segundo par: anterior 1020, agora 10. O ponteiro deu a volta pelo tamanho 1024. Isso é TC. HT não substitui essa leitura. A ISR que faz feature aqui dentro estoura jitter; a transferência ADC→memória sem CPU por amostra é o DMA do fill. Os inteiros são contadores de bancada, não amostras de uma pessoa. Errar HT/TC duplica bloco ou pula bloco — o ring downstream não perdoa.

Fase F9, nt-fw-irq-dma: (520, 500) é HT sem TC; (10, 1020) é TC. Half=512 e full=1024. A ISR longa é o jitter do MCQ; a conta aqui é só qual limiar o ponteiro cruzou.
