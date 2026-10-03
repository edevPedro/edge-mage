# História — Os Vinte e Quatro Bits do Silício

Na bancada de montagem eletrônica, um desenvolvedor conecta uma placa OpenBCI Cyton a uma bateria de polímero de lítio de 3.7 V. A placa é o padrão aberto mais difundido no ecossistema de neuroengenharia, equipada com um microcontrolador PIC32 e um conversor analógico-digital Texas Instruments ADS1299 de 24 bits e 8 canais.

O desenvolvedor abre o terminal serial e observa o fluxo hexadecimal contínuo transmitido a 250 Hz pelo módulo de rádio:
```text
41 01 02 A3 04 05 FF FE 10 ... C0
```

Ele tenta converter os bytes recebidos em números inteiros, mas os valores resultantes oscilam de forma caótica:
```python
# Erro de parsing: tratando 24 bits em complemento de dois como uint24
val = (b[0] << 16) | (b[1] << 8) | b[2]
```

— Observe o formato de transmissão do ADS1299 — explica o engenheiro de hardware do laboratório. — O conversor digitaliza biopotenciais com 24 bits de resolução em formato de complemento de dois com sinal (signed two's complement). Ele transmite três bytes por amostra em ordem big-endian: o byte mais significativo (MSB) carrega o bit de sinal no bit 23. Se esse bit for 1, o número é negativo!

O engenheiro demonstra o algoritmo de extensão de sinal (sign extension):
— Se você apenas juntar os três bytes em um inteiro de 32 bits sem estender o bit de sinal para os bits 24 a 31, um biopotencial negativo de $-50\ \mu\text{V}$ (cujo valor em 24 bits é `0xFFFFCE`) será interpretado pelo Python como um número positivo gigantesco de $+16.777.166$, explodindo instantaneamente qualquer filtro digital!

Ele ensina a rotina correta: se o bit 23 estiver ativo (`val & 0x800000`), subtrai-se $2^{24} = 16.777.216$ para restaurar o valor negativo autêntico com sinal (`parse_24bit_signed`).

O desenvolvedor implementa a conversão e multiplica pela escala do conversor ($V_{\text{ref}} / (\text{Ganho} \times 2^{23})$). O sinal temporal estabiliza-se em microvolts limpos, revelando o traçado fisiológico impecável dos canais de escalpo.
