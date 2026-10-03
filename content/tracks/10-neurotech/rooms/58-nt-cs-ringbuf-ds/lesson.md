# Lição — Ring buffer

## Objetivos
Dominar estrutura circular para stream EEG o suficiente para o pilar e a espinha BCI.

## Passos
1. Leia o conceito e anote 5 termos-chave.
2. Faça 1 exercício numérico ou de design ligado à Sala.
3. Escreva uma honesty note (limites do que esta sala *não* cobre).
4. Ligue esta sala à anterior e à próxima no mapa do portal.

## Lab
Explique em 6–10 linhas como estrutura circular para stream EEG aparece num pipeline MI offline ou online.

## Checklist
- [ ] Conceito lido
- [ ] Lab anotado
- [ ] Pronto para a Sala

## Numeric / fill warm-up
Escreva: definição → fórmula ou diagrama → falha típica → ligação a decode/online.

Para destravar o lab, abra [Wikipedia — Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer) e leia a política de overwrite do buffer circular (cabeça e cauda, capacidade fixa) para latest() devolver o último valor e não crescer o vetor.

## Lab estendido (obrigatório no Estuda)

1. Produza um artefato (tabela, diagrama ASCII ou pseudo-código ≤20 linhas) cobrindo o núcleo desta sala.
2. Calcule ou estime **um** número com unidade (Hz, µV, ms, dB, κ, Big-O, etc.).
3. Escreva a honesty note em 2 frases.
4. Liste pré-requisitos cumpridos (`requires_rooms`) e o que desbloqueia a seguir.
