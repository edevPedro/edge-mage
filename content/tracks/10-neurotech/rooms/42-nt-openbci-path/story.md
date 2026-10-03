# História — Os três bytes do ADS1299 didático

Sem a placa, o caminho honesto continua sendo o emulador. Quem mesmo assim lê um pacote Cyton precisa do inteiro de 24 bits com sinal. O guardião dita três chamadas de `parse_24bit_signed(b0, b1, b2)`.

`(0, 0, 1)` é 1. `(0xFF, 0xFF, 0xFF)` é −1, não 16777215: o bit 23 é sinal, complemento de dois. `(0x7F, 0xFF, 0xFF)` é o máximo positivo, `2^23 − 1 = 8388607`. Tratar os bytes como unsigned grande entrega 16777215 no caso dos FF e falha.

A ordem dos bytes é a do pacote, MSB primeiro, como no teste. Isto não calibra eletrodo, não cria um EEG de pessoa e não substitui o Getting Started. A conta é o inteiro com sinal; a sala eletiva só abre quando os três valores batem, placa presente ou não.

Eletivo nt-openbci-path: os três inteiros são 1, −1 e 8388607. O bit 23 é sinal. Sem a placa, o emu continua sendo o caminho honesto; o parser não cria EEG humano.
