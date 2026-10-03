# História — O pico que escolhe a frequência

Eletivo, não portão do Supremo. Três frequentes de estímulo, 10, 12 e 15 Hz, e um espectro de bancada com potências `[2,0, 18,5, 3,0]` nos mesmos bins. O guardião pede `ssvep_detect`: entre os alvos, a frequência cuja potência é máxima.

18,5 é o maior dos três; o bin correspondente é 12 Hz. Devolver 18,5 é entregar potência, não frequência. Devolver 15 porque “é o maior Hz” ignora a potência. A resposta da Sala é `12.0`.

SSVEP é resposta evocada em frequência de flicker, outro paradigma — não é ERD de imagética e não é leitura de intenção clínica. Se duas potências empatam, a função precisa de regra estável; aqui não há empate. O review de Zhu está no resource para a definição do paradigma, não para colar um ITR de paper neste vetor de três números.

Eletivo nt-ssvep-elective: ssvep_detect devolve 12.0, a frequência, não 18.5. Potência máxima no alvo errado troca o comando do flicker; este vetor não é um ITR publicado.
