# Lição — Testes realtime

## Objetivos

Desenhar 3 testes de stream; definir métricas underrun/deadline.

## Passos

1. Pseudo-teste: push 250 samples/s, consumer a 1 janela/40 ms — detectar underrun.
2. Assert: p95 latency < deadline.
3. Relacione leak de CV (offline) vs bug de timing (online) — falhas diferentes.

## Lab

Escreva um checklist de CI para `mage emu online`.

## Checklist

- [ ] Underrun definido
- [ ] Deadline testável
- [ ] Pronto para filter-bank / stream

Para destravar o lab, abra [Varoquaux et al. — CV pitfalls](https://doi.org/10.1016/j.neuroimage.2016.10.038) e leia o aviso de Varoquaux contra avaliação que vaza, para timing_analysis contar miss no intervalo e não “ajustar” o relógio no teste.

## Lab estendido (obrigatório no Estuda)

1. Produza um artefato (tabela, diagrama ASCII ou pseudo-código ≤20 linhas) cobrindo o núcleo desta sala.
2. Calcule ou estime **um** número com unidade (Hz, µV, ms, dB, κ, Big-O, etc.).
3. Escreva a honesty note em 2 frases.
4. Liste pré-requisitos cumpridos (`requires_rooms`) e o que desbloqueia a seguir.
