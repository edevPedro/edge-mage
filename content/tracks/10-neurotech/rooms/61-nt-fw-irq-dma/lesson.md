# Lição — IRQ/DMA

## Objetivos
Dominar amostragem sem busy-wait o suficiente para o pilar e a espinha BCI.

## Passos
1. Leia o conceito e anote 5 termos-chave.
2. Faça 1 exercício numérico ou de design ligado à Sala.
3. Escreva uma honesty note (limites do que esta sala *não* cobre).
4. Ligue esta sala à anterior e à próxima no mapa do portal.

## Lab
Explique em 6–10 linhas como amostragem sem busy-wait aparece num pipeline MI offline ou online.

## Checklist
- [ ] Conceito lido
- [ ] Lab anotado
- [ ] Pronto para a Sala

## Numeric / fill warm-up
Escreva: definição → fórmula ou diagrama → falha típica → ligação a decode/online.

Para destravar o lab, abra [ARM Cortex-M generic interrupt model (CMSIS docs hub)](https://www.keil.com/pack/doc/CMSIS/Core/html/index.html) e leia o modelo de interrupção do CMSIS (ISR curta, flag de metade e de completo) para check_dma_irq separar HT de TC.

## Lab estendido (obrigatório no Estuda)

1. Produza um artefato (tabela, diagrama ASCII ou pseudo-código ≤20 linhas) cobrindo o núcleo desta sala.
2. Calcule ou estime **um** número com unidade (Hz, µV, ms, dB, κ, Big-O, etc.).
3. Escreva a honesty note em 2 frases.
4. Liste pré-requisitos cumpridos (`requires_rooms`) e o que desbloqueia a seguir.
