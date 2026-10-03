# História — O Ganho Oculto no Filtro Espacial

Na bancada de integração de hardware-in-the-loop, um desenvolvedor recém-chegado do ecossistema de APIs web observa o monitor serial de um firmware de BCI. O streamer envia amostras de quatro eletrodos de escalpo — $C3$, $Cz$, $C4$ e $Pz$ — digitalizadas a 250 Hz. O objetivo do sprint é implementar uma montagem de filtro espacial para realçar a dessincronização relacionada a evento (ERD) no canal $C3$ durante a imagética motora da mão contralateral.

O desenvolvedor define um vetor de pesos artesanal baseado em uma vizinhança discreta: $w = [3.0, 4.0]$. Ele alimenta a rotina de projeção linear $s = \langle w, x \rangle$, esperando que o produto interno entregue um sinal limpo centrado na mesma ordem de grandeza dos sinais brutos ($10\text{--}40\ \mu\text{V}$). 

No entanto, o classificador linear a jusante entra imediatamente em overflow numérico: todas as predições travam na classe 1. Olhando o osciloscópio digital, o engenheiro sênior de sistemas aponta para o erro conceitual: o vetor de pesos $[3.0, 4.0]$ tem norma euclidiana $\|w\|_2 = \sqrt{3^2 + 4^2} = 5.0$. Sem a divisão pelo comprimento do vetor, o filtro espacial estava multiplicando a energia de cada amostra por cinco, gerando amplitudes de centenas de microvolts que explodiam os limiares calibrados.

Para restabelecer a integridade biofísica do sinal, o desenvolvedor é desafiado a implementar a normalização estrita de energia: derivar $\hat{w} = w / \|w\|_2$, garantindo que a projeção preserve a escala unitária do espaço euclidiano antes de qualquer decisão algorítmica.
