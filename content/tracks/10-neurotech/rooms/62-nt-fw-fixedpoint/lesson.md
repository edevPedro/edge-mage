# Lição — Fixed-point

## Objetivos
Dominar Q15 o suficiente para o pilar e a espinha BCI.

## Passos
1. Leia o conceito e anote 5 termos-chave.
2. Faça 1 exercício numérico ou de design ligado à Sala.
3. Escreva uma honesty note (limites do que esta sala *não* cobre).
4. Ligue esta sala à anterior e à próxima no mapa do portal.

## Lab
Explique em 6–10 linhas como Q15 aparece num pipeline MI offline ou online.

## Checklist
- [ ] Conceito lido
- [ ] Lab anotado
- [ ] Pronto para a Sala

## Numeric / fill warm-up
Escreva: definição → fórmula ou diagrama → falha típica → ligação a decode/online.

Para destravar o lab, abra [CMSIS-DSP fixed-point overview](https://www.keil.com/pack/doc/CMSIS/DSP/html/index.html) e leia a convenção Q15 do CMSIS-DSP (15 bits de fração, saturação no int16) para float_to_q15 mapear 0,5 em 16384 e grampear acima de 1.

## Lab estendido (obrigatório no Estuda)

1. Produza um artefato (tabela, diagrama ASCII ou pseudo-código ≤20 linhas) cobrindo o núcleo desta sala.
2. Calcule ou estime **um** número com unidade (Hz, µV, ms, dB, κ, Big-O, etc.).
3. Escreva a honesty note em 2 frases.
4. Liste pré-requisitos cumpridos (`requires_rooms`) e o que desbloqueia a seguir.
