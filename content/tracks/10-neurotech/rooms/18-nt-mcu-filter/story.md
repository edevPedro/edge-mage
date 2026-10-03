# História — O MAC que saturou em Q15

O stub de MCU não é filter-bank de MI. Na bancada Q15, o guardião pede `q15_mac(acc, a, b) = acc + ((a * b) >> 15)`, com saturação em `[−32768, 32767]`.

Primeiro ensaio: `acc = 0`, `a = b = 16384`. O produto é `16384² = 268435456`. O deslocamento de 15 bits divide por 32768 e entrega 8192. Quem esquecer o `>> 15` devolve o produto cru e estoura o formato.

Segundo ensaio: `q15_mac(30000, 32767, 32767)`. `(32767² >> 15)` já é 32766; somado a 30000 passa de 32767. Sem saturação o acumulador vira lixo com sinal; com saturação a Sala exige 32767. Isto é MAC fracionário de laboratório, não um FIR de ritmos nem um claim de que o Cortex já decodifica imagética.

Fase F9, nt-mcu-filter: q15_mac(0, 16384, 16384) tem de cair em 8192, e o segundo ensaio satura em 32767. Sem o shift de 15 o produto não é Q15; sem o grampo o acumulador muda de sinal.
