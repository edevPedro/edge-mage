# História — O prêmio que não desce abaixo de zero

Neurofeedback aqui é feedback de banda em circuito fechado de laboratório, não prescrição. O guardião recusa a frase terapêutica. A função `nfb_reward(atual, baseline, scale)` devolve `max(0, (atual − baseline) * scale)`.

Alfa de bancada 15 contra baseline 10, escala 10: `(15 − 10) * 10 = 50`. Alfa 8 contra a mesma baseline: diferença negativa, o `max` corta em `0`. Devolver −20 “porque a conta deu isso” recompensa a descida e inverte o feedback.

A banda occipital clássica do fill é alfa — não porque esta função trate um sujeito, mas porque o paradigma publicado usa esse nome. 50 e 0 são unidades de feedback do toy. Gruzelier está no resource como review para o limite do claim, não como autorização para dizer que o 50 melhora alguém.

Fase F11, nt-app-neurofeedback: recompensa 50 acima da baseline e 0 abaixo. A banda do fill é alfa. Prescrever terapia está fora; o max(0, ·) só impede feedback com sinal trocado.
