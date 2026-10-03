# História — O anel que sobrescreveu o começo

O decoder online pede as últimas amostras enquanto o produtor não para. O guardião instancia `RingBuffer` com capacidade 3 e empurra, em ordem, 0, 1, 2, 3 e 4. A aprendiz lê `latest(10)` e espera os cinco valores.

Não cabem. A política é overwrite: 0 e 1 já saíram. Os três mais recentes, do mais antigo ao mais novo, são `[2, 3, 4]`. `latest(3)` devolve a mesma lista; `latest(10)` não inventa amostra que o anel não guarda.

Underrun é o outro erro — pedir 500 quando só há 120 — mas nesta bancada o buffer está cheio e a falha é achar que capacidade cresce. Ordem antiga→nova importa: `[4, 3, 2]` quebra o filtro que vem depois. Unidade: amostra no anel, não milissegundo. O synth não é um sujeito esperando na cadeira.

Fase F9, nt-stream-buffer: depois de cinco push numa capacidade 3, tanto latest(3) quanto latest(10) valem [2, 3, 4]. Capacidade não estica, e a ordem antiga→nova é parte do contrato do anel.
