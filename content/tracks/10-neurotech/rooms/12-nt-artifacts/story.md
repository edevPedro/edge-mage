# História — O limiar que não é um ritmo

A bancada de artefatos entrega o trecho sintético `[10, −150, 20, 110]`, em unidades do vetor, não um traçado de sujeito. O guardião pede `flag_artifacts` com limiar 100: marque o índice onde o módulo passa de 100.

A aprendiz aponta o 10 “porque é o começo”. Errado. `|10|` fica, `|-150| = 150` cai no índice 1, `|20|` fica, `|110|` cai no índice 3. A lista é `[1, 3]`, não os valores, não os índices pares.

Linha de rede, 50 ou 60 Hz, é outro artefato — não entra nesta conta. Rejeitar o trial extremo é higiene do pipeline; fingir que o pico é mu é como treinar o classificador em piscada. O synth continua sintético: limiar alto demais zera a lista, limiar 100 sem módulo absoluto esquece o −150.

Fase F6, nt-artifacts: flag_artifacts devolve índices, não cópia do sinal. Limiar 100 com a lista da bancada tem de produzir exatamente dois índices; um a mais significa que você comparou o valor cru, não o módulo.
