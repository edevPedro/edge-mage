# História — O passo que dispara e o que não é EEG

HH fica como mapa mental: sódio sobe, potássio repolariza, limiar regenera. A Sala não integra o HH completo. Integra um LIF explícito, Euler, `dt = 0,001 s`, `τ = 20 ms`, `R = 10`, repouso −70 mV, limiar −55 mV.

`v_next = v + (dt/τ) * (−(v − v_rest) + R * I)`. Em `v = −70` e `I = 0` o incremento é zero: devolve `(−70, False)`. Em `v = −56` e `I = 10`, o termo entre parênteses é `−(−56 − (−70)) + 100 = 86`. Vezes `0,001/0,020 = 0,05` dá `+4,3`. `−56 + 4,3 = −51,7`, que cruza −55: a função devolve o reset `(−70, True)`, não o −51,7.

Esse spike de brinquedo não é um potencial de escalpo. EEG é população filtrada pelo volume. A honesty da sala é exatamente essa: sem geometria, sem rede HH, sem single-unit no eletrodo de superfície.

Fase F4, nt-neuro-neuron-hh: o primeiro passo fica em −70 mV sem spike; o segundo reseta a −70 mV com spike True. Guardar −51,7 é esquecer o limiar. EEG de escalpo não é esse AP.
