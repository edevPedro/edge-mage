# História — O inteiro que representa meio

Q15 guarda fração em 15 bits, sinal no 16º. `float_to_q15` mapeia `[-1, 1)` para `[−32768, 32767]` e satura fora.

`0,5 * 32768 = 16384`. Esse é o primeiro ensaio. `−1,0` cai no mínimo do int16, `−32768`, não em −32767: o extremo negativo tem um código a mais. `1,5` não cabe; satura em `32767`. Devolver 49152, ou deixar estourar para negativo, é o bug que a sala de MAC já mostrou.

`1,0` cheio, se aparecesse, não tem código positivo simétrico — por isso o intervalo é meio-aberto do lado positivo. Unidade: LSB de Q15, não volt. Sem saturação, o FIR do stub embrulha o ritmo numa rampa falsa. A conta desta cena é só a conversão: 16384, −32768 e 32767, nessa ordem de ensaio.

Fase F9, nt-fw-fixedpoint: 0,5 vira 16384, −1 vira −32768, 1,5 satura em 32767. O formato do fill chama-se Q15. Sem grampo, o overflow troca o sinal do acumulador.
