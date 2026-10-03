# Conceito — Protocolo OpenBCI Cyton e Decodificação de Inteiros de 24 Bits com Sinal

O hardware OpenBCI Cyton utiliza o front-end analógico ADS1299 da Texas Instruments, padrão-ouro para biopotenciais não-invasivos.

## 1. O Pacote de Dados Padrão do Cyton (33 Bytes)
A placa transmite pacotes de tamanho fixo a 250 Hz:
- **Byte 0:** Byte de cabeçalho (`0xA0`).
- **Byte 1:** Contador de amostras (0 a 255 com wrap-around).
- **Bytes 2 a 25:** 8 canais de EEG (3 bytes por canal = 24 bits em complemento de dois, big-endian).
- **Bytes 26 a 31:** Dados auxiliares (acelerômetro de 3 eixos ou marcadores de trigger digital).
- **Byte 32:** Byte de rodapé (stop byte).

## 2. Decodificação de Inteiros de 24 Bits com Extensão de Sinal
Dada uma trinca de bytes `(b0, b1, b2)` em ordem big-endian:
1. Concatenação dos bytes:
   $$\text{raw} = (b_0 \ll 16) \mid (b_1 \ll 8) \mid b_2$$
2. Verificação do bit de sinal (bit 23):
   $$\text{Se } (\text{raw} \;\&\; 0x800000) \ne 0: \quad \text{valor} = \text{raw} - 2^{24}$$
   $$\text{Caso contrário}: \quad \text{valor} = \text{raw}$$

## 3. Conversão para Volts / Microvolts
Para converter o inteiro decodificado em volts reais:
$$\text{Tensão (V)} = \text{valor} \times \left( \frac{V_{\text{ref}}}{\text{Ganho} \times (2^{23} - 1)} \right)$$
Com $V_{\text{ref}} = 4.5\text{ V}$ e ganho padrão de $\times 24$:
$$\text{Escala LSB} = \frac{4.5}{24 \times 8388607} \approx 0.02235\ \mu\text{V} / \text{count}$$

## 4. Modos de Falha na Prática de Engenharia
1. **Omissão da Extensão de Sinal:** Provoca descontinuidades extremas sempre que o sinal cruza a linha de zero volts, injetando degraus de $16$ milhões de counts no filtro digital.
2. **Perda de Pacotes por Driver Serial:** Ler o buffer da porta serial sem checagem de integridade de cabeçalho (`0xA0`) e contador de amostras contíguo.

## O Que a Próxima Sala Assume
Parabéns! Esta sala conclui integralmente o catálogo de 77 salas da trilha de Neuroengenharia do edge-mage, formando uma ponte sólida e rigorosa entre a engenharia convencional de software e a neurotecnologia aplicada.

## Artigos de Apoio e Leituras Recomendadas
- [OpenBCI Cyton Getting Started](https://docs.openbci.com/GettingStarted/Boards/CytonGS/) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [OpenBCI EEG Setup](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
