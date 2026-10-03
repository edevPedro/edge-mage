# História — O buraco na sequência

O harness não discute estilo: conta pacote perdido. `detect_drops(seqs, max_seq=256)` olha saltos. Lista `[0, 1, 2, 3]` não tem buraco: 0. Lista `[0, 2, 3]` saltou o 1: um drop.

O caso que pega o novato é o wrap: `[255, 1]` com `max_seq = 256`. De 255 o próximo esperado é 0, depois 1. Chegar em 1 implica que 0 não apareceu: um drop, não “sequência válida porque 1 é pequeno”. Tratar como inteiros sem módulo conta `1 − 255` e inventa um buraco absurdo, ou conta zero e esconde a perda.

Zero drops no primeiro vetor é tão obrigatório quanto o um nos outros. Cada drop é amostra que o ring não vai reconstruir. Não é métrica de κ. Seed e assert continuam sendo o contrato: se o PR aumenta drop no synth, o teste quebra de propósito.

Fase F5, nt-cs-harness: drops valem 0, 1 e 1 nos três ensaios, e o wrap 255→1 com max_seq 256 conta o 0 ausente. Assert que ignora módulo esconde perda de pacote.
