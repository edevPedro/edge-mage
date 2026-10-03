# História — A média que não é um periodograma só

Dois segmentos já viraram espectros de potência. O guardião não pede FFT de novo: pede `welch_average` da lista `[[1, 2, 3], [3, 4, 5]]`.

Bin a bin: `(1+3)/2 = 2`, `(2+4)/2 = 3`, `(3+5)/2 = 4`. A Sala confere os dois primeiros bins, 2 e 3. Quem devolve o primeiro segmento, ou a soma sem dividir, falha. A média é o que reduz variância no Welch; um único periodograma continua ruidoso.

Ao lado, a resolução: segmento de `T = 2,0 s` tem `Δf ≈ 1/T = 0,5 Hz`. Não confunda esse 0,5 Hz com o bin 2 de potência — unidades diferentes. Vazamento espectral não se cura aumentando o claim: o número honesto é a média dos segmentos que você de fato tem, com a janela declarada.

Fase F6, nt-dsp-welch: a média dos dois espectros começa em 2 e 3; o terceiro bin é 4. Δf de um segmento de 2 s é 0,5 Hz — não escreva 0,5 no vetor de potência.
