# Lição — RT firmware

## Objetivos

1. Desenhar ISR magra + deferred filter.
2. Definir overrun/underrun no MCU path.
3. Declarar limites do stub.

## Passos

1. Timeline: DRDY → DMA → ringbuf → task FIR → UART.
2. Calcule: fs=250, budget=4 ms; se FIR leva 3 ms média e às vezes 5 ms, o que falha?
3. Honesty note no caderno.

## Checklist

- [ ] ISR magra
- [ ] Buffer strategy
- [ ] Stub ≠ QEMU

Para destravar o lab, abra [TI ADS1299 datasheet](https://www.ti.com/lit/ds/symlink/ads1299.pdf) e leia a taxa de amostragem e o relógio de dados do ADS1299 para rt_safe aplicar a folga de 20% sobre o deadline em µs.

## Lab estendido (obrigatório no Estuda)

1. Produza um artefato (tabela, diagrama ASCII ou pseudo-código ≤20 linhas) cobrindo o núcleo desta sala.
2. Calcule ou estime **um** número com unidade (Hz, µV, ms, dB, κ, Big-O, etc.).
3. Escreva a honesty note em 2 frases.
4. Liste pré-requisitos cumpridos (`requires_rooms`) e o que desbloqueia a seguir.
