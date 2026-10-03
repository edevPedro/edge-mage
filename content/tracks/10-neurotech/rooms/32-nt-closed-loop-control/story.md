# História — O alfa que segurou o comando

Feedback agressivo em cima de label cru oscila. O guardião pede o primeiro passo de `ema_update(current, prev, alpha)` com `alpha = 0,2`, valor atual 1,0 e suavizado anterior 0,0.

`0,2 * 1,0 + (1 − 0,2) * 0,0 = 0,2`. Não é 1,0 — isso seria seguir o cru. Não é 0,0 — isso seria ignorar a medida. O complemento `(1 − alpha)` pesa a memória; trocar os pesos entrega `0,8` e a Sala recusa.

Unidade: a mesma do sinal de comando, adimensional neste toy. Atraso grande mais ganho alto instabiliza o loop; a EMA é o amortecedor didático, não um controlador clínico. Orçamento sense/decide/act continua em milissegundos, noutra task. Sem sujeito: o 0,2 só prova que você aplicou a recorrência certa antes de fechar o atuador simulado.

Fase F9, nt-closed-loop-control: ema_update(1, 0, 0,2) devolve 0,2. O orçamento do loop continua em ms; o 0,2 só mostra que o ganho e a memória foram para os termos certos.
