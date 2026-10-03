# História — O máximo dentro da janela, não no vetor

Oddball: estímulo raro entre frequentes. A Sala não reproduz o speller de Farwell e Donchin; pede o pico positivo num vetor sintético. Duzentos zeros. No índice 75, o valor 12,5. `fs = 250`, janela de 250 ms a 450 ms.

Índice 75 em 250 Hz é `75/250 * 1000 = 300 ms`, dentro da janela. O máximo nesse intervalo é 12,5. Um pico fora, mesmo maior, não conta. Devolver o índice 75 em vez do valor falha. Devolver 0 porque “a média é zero” ignora a deflexão.

12,5 é amplitude do vetor de bancada, não um µV de pessoa nem um diagnóstico de atenção. A janela 250–450 ms é a do código, alinhada ao clássico, não uma medida sua. Sem oddball declarado, o pico nem tem paradigma. A honesty: emulação educacional, não um speller clínico.

Fase F11, nt-app-hybrid-p300: o pico na janela 250–450 ms, índice 75, vale 12,5. O fill do paradigma é oddball. Fora da janela o máximo não entra, e o vetor não é um speller de sujeito.
