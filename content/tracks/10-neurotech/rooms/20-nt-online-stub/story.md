# História — As janelas que escorregam

O loop online não relê o arquivo inteiro. O guardião fixa `sliding_windows` com `win_len = 250` e `hop = 50` e pede os pares `(start, end)` até cobrir o trecho que o teste usa.

A primeira janela é `(0, 250)`. A segunda começa no hop: `(50, 300)`. A terceira: `(100, 350)`. Fim exclusivo: cada janela tem 250 amostras, não 250 de índice inclusivo. Hop 50 não é overlap zero — o overlap é 200 amostras.

À parte, 25 amostras a `fs = 250 Hz` duram `25/250 * 1000 = 100 ms`. Essa conta é a task numérica da sala; não misture com o comprimento 250 da janela de código. Miss continua sendo latência acima do budget. O emulator não tem sujeito: κ offline alto não prova que estes índices cabem no deadline.

Fase F9, nt-online-stub: os três primeiros pares são (0, 250), (50, 300) e (100, 350). O fim é exclusivo. Os 100 ms da janela de 25 amostras a 250 Hz são outra linha do caderno, não o hop.
