# História — O lambda que só toca a diagonal

Duas covariâncias quase singulares não se invertem no grito. O guardião entrega `[[1,0, 0,5], [0,5, 1,0]]` e pede `regularize_matrix` com `lambda = 0,1`: somar o termo só na diagonal.

`(0,0)` vai a `1,0 + 0,1 = 1,1`. `(1,1)` vai a `1,1`. O fora da diagonal permanece `0,5`. Somar 0,1 na matriz inteira suja a covariância e falha o teste. Usar o default `1e-3` em vez de 0,1 também falha: a Sala passou o lambda de propósito.

Isto é shrinkage / Tikhonov de laboratório, não um estimador de paper. Cancelamento de float — subtrair números quase iguais — é o outro aviso da sala, e o formato de MCU chama-se fixed-point, não “inteiro mágico”. Unidade do lambda: a mesma da diagonal. Sem essa soma, o log-var e o CSP toy herdam matriz doente.

Fase F5, nt-cs-numerics: diagonal 1,1 e 1,1, fora-diagonal 0,5, com lambda 0,1. Fixed-point é o nome do fill para a fração em inteiro. Somar lambda fora da diagonal falha o harness.
