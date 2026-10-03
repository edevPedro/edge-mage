# História — O alfa que vale um no pico

A ponte do spike ao LFP passa pela condutância sináptica, não por um AP desenhado no escalpo. O guardião pede `alpha_conductance(t, tau, g_peak)`: `g_peak * (t/τ) * exp(1 − t/τ)` para `t ≥ 0`.

No pico pedagógico, `t = τ = 0,005` e `g_peak = 1`. `(t/τ) = 1`, `exp(1 − 1) = exp(0) = 1`, logo a condutância é 1. Em `t = 0` o fator `t/τ` zera o produto, mesmo com o exponencial: a Sala exige ~0, não `g_peak`.

EPSP é excitatório; IPSP, inibitório. Correntes sinápticas sincronizadas é que pesam no LFP — a frase do MCQ — e não um neurônio isolado. Unidade desta conta: a mesma de `g_peak`, com tempo em segundos. Nada aqui é um traçado de paciente; é a forma de alfa que o filtro de população vai somar.

Fase F4, nt-neuro-synapse: no instante t=τ a condutância alfa vale g_peak (1); em t=0 vale 0. EPSP nomeia o fill — excitatório — e o LFP soma essas correntes, não o spike isolado.
