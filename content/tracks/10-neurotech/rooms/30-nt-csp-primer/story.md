# História — A variância que era zero

O primer de CSP não pede o autovetor generalizado completo. Pede `spatial_filter_logvar(epoch, w)` num toy que denuncia piso numérico. Epoch com dois canais constantes: `[[1, 1], [2, 2]]`. Pesos `w = [1, 0]` — só o canal 0 entra.

`y[t] = 1 * epoch[0][t]`, logo `y = [1, 1]`. A variância de um vetor constante é 0. O log de zero não é feature: a Sala usa `ln(var + 1e-6) = ln(1e-6)`. Quem devolve `ln(1)` porque “o sinal vale 1”, ou variância populacional com o canal 2 misturado, erra o teste.

Feature clássica depois do filtro espacial continua sendo log-variância, estimada no treino, não no teste com label vazado. Este toy não é um κ de paper CSP. Filtro com peso no canal errado muda `y` para `[2, 2]` e a variância segue 0 — o piso aparece de novo, mas o vetor projetado não é o que o guardião pediu.

Fase F8, nt-csp-primer: com y constante a variância é 0 e o log-var da Sala é ln(1e-6). Os filtros estimam-se no treino; este toy só trava o piso numérico antes de qualquer κ.
