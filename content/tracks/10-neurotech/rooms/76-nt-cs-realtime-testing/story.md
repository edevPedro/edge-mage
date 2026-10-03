# História — O jitter médio e o único miss

Tempo real se testa com relógio, não com esperança. Carimbos `[0, 0,004, 0,008, 0,014]` segundos. Alvo `0,004 s`, miss se `|dt − alvo| > 0,001`.

Intervalos: `0,004`, `0,004` e `0,006`. Desvios absolutos: `0`, `0` e `0,002`. A média é `(0 + 0 + 0,002) / 3 = 0,002/3`. Misses: só o terceiro passa de 1 ms, então `m = 1`. Contar os três intervalos como miss, ou dividir por quatro carimbos em vez de três deltas, quebra o assert.

`0,002/3` segundos é jitter médio, não latência de ponta a ponta. Deadline segue sendo o nome do orçamento sense→decide→act. Um miss neste harness é o teste útil de loop; não é evidência de que um device real segurou o prazo. Varoquaux, no resource, freia outro vazamento — o de validação — para você não “consertar” o jitter vazando o teste.

Fase F5, nt-cs-realtime-testing: um miss e jitter médio 0,002/3 s. O fill do orçamento chama-se deadline. Dividir pelos carimbos em vez dos intervalos dilui o erro e o teste deixa de pegar o atraso.
