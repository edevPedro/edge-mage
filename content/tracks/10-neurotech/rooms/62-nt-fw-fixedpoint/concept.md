# Conceito — Aritmética de Ponto Fixo Q15 e Saturação em Microcontroladores

## 1. Por Que Ponto Fixo em Neurotecnologia Embarcada?
Dispositivos portáteis ou vestíveis de EEG (como faixas de sono ou fones neurais) frequentemente adotam microcontroladores de baixo custo e baixíssimo consumo (ARM Cortex-M0, Cortex-M3). Esses chips não possuem Unidade de Ponto Flutuante (*Floating Point Unit* - FPU):
- Uma operação de `float` consome entre 20 e 80 ciclos de relógio via biblioteca de emulação de software (`libgcc`/`soft-fp`).
- Uma operação de ponto fixo em registradores de 16 bits (`int16_t`) executa em **1 único ciclo de clock**, consumindo ordens de magnitude menos energia.

## 2. O Formato Numérico Q15
O formato Q15 representa números fracionários com sinal no intervalo $[-1.0, +1.0)$ utilizando um inteiro signed de 16 bits em complemento de dois:
- **Bit 15:** Bit de sinal ($0 = \text{positivo}$, $1 = \text{negativo}$).
- **Bits 0 a 14:** 15 bits para a parte fracionária.
- **Fator de Escala:** $2^{15} = 32768$.
- **Resolução (LSB):** $\Delta = 2^{-15} = \frac{1}{32768} \approx 3.0517578 \times 10^{-5}$.

### Mapeamento Matemático:
$$\text{Inteiro Q15} = \text{round}(x \times 32768)$$

| Valor em Ponto Flutuante | Valor Inteiro Q15 | Representação Hexadecimal |
| :--- | :--- | :--- |
| $-1.0$ (Mínimo exato) | $-32768$ | `0x8000` |
| $-0.5$ | $-16384$ | `0xC000` |
| $0.0$ | $0$ | `0x0000` |
| $+0.5$ | $+16384$ | `0x4000` |
| $+0.99996948$ (Máximo exato) | $+32767$ | `0x7FFF` |

Note que o valor $+1.0$ exato não pode ser representado em Q15 (exigiria 16 bits de fração além do sinal); ele satura naturalmente no valor máximo positivo $+32767$.

## 3. O Perigo do Overflow e Aritmética Saturada
Em complemento de dois de 16 bits sem saturação:
$$32767 + 1 = -32768$$
Essa inversão brusca de sinal desestabiliza filtros digitais recursivos (IIR), gerando oscilações de alta frequência que destroem a decodificação neural.
A saturação (*saturation arithmetic*) força a limitação estrita:
$$x_{sat} = \min(32767, \max(-32768, x_{scaled}))$$

## O Que a Próxima Sala Assume
A próxima sala (`nt-fw-aarch64-bridge`) — **Embedded — Ponte AArch64 / Edge** — acelera operações de álgebra linear espacial utilizando instruções vetoriais SIMD de 128 bits (Arm Neon).

## Artigos de Apoio e Leituras Recomendadas
- [CMSIS-DSP fixed-point overview](https://www.keil.com/pack/doc/CMSIS/DSP/html/index.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [ARM CMSIS Core docs](https://www.keil.com/pack/doc/CMSIS/Core/html/index.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
