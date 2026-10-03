# Desafio — Decodificação de Inteiros de 24 Bits em Complemento de Dois

## 1. Objetivo do Desafio
Implementar a rotina de baixo nível para conversão de trincas de bytes brutas de protocolo de hardware (ADS1299/OpenBCI) em inteiros com sinal de 24 bits através de extensão de sinal.

## 2. Especificação Técnica e Formulação
Dada uma tupla ou lista de três bytes inteiros `(b0, b1, b2)` no intervalo $[0, 255]$ em ordem big-endian:
- Implemente a função `parse_24bit_signed(bytes_tuple)`:
  1. Concatene os bits: $\text{val} = (b_0 \ll 16) | (b_1 \ll 8) | b_2$.
  2. Verifique o bit 23 (`val & 0x800000`). Se for 1, o número é negativo: subtraia $2^{24} = 16777216$.
  3. Retorne o valor inteiro resultante com sinal (positivo ou negativo).

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que a trinca `(0x00, 0x00, 0x01)` retorne `+1`.
- A trinca `(0xFF, 0xFF, 0xFF)` deve retornar `-1`.
- A trinca `(0x7F, 0xFF, 0xFF)` deve retornar `+8388607` (maior positivo).
- A trinca `(0x80, 0x00, 0x00)` deve retornar `-8388608` (menor negativo).
