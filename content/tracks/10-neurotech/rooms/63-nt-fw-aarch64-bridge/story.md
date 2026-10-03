# História — Quatro lanes, um escalar

A ponte para o Edge não pede um kernel NEON real. Pede `simd4_dot(a, b)`, o produto escalar de quatro lanes, como uma instrução larga faria numa tacada.

`a = [1, 2, 3, 4]`, `b = [2, 0, 1, −1]`. Lane a lane: `1*2 = 2`, `2*0 = 0`, `3*1 = 3`, `4*(−1) = −4`. Soma: `2 + 0 + 3 − 4 = 1`. Esquecer o sinal do último termo entrega 9. Somar só os dois primeiros entrega 2.

1 é o escalar da Sala, não um score de BCI e não um ciclo de CPU medido. Documentar stub versus device real é o fill da ponte: este dot roda no host. A ISA AArch64 profunda continua no curso Edge; aqui o erro é aritmético. Quatro lanes erradas viram feature errada no mesmo pacote que o DMA acabou de fechar.

Fase F9, nt-fw-aarch64-bridge: o dot de quatro lanes fecha em 1. O fill da ponte é gap (stub versus device). Nove significa que o −4 virou +4 — o sinal da lane é parte da instrução.
