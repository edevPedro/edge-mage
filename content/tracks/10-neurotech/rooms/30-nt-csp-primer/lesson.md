# Lição — CSP primer

## Pipeline

epochs → band-pass → cov por classe → CSP → log-var → LDA/SVM

## Armadilhas

- CSP overfitting com poucos trials
- Fit CSP só no treino (vazamento se usar teste)

Para destravar o lab, abra [Ramoser et al. IEEE TNSRE 2000 — CSP](https://doi.org/10.1109/86.895946) e leia a feature log-variância depois do filtro espacial em Ramoser, para spatial_filter_logvar usar o piso 1e-6 quando a projeção é constante.

## Lab estendido (obrigatório no Estuda)

1. Produza um artefato (tabela, diagrama ASCII ou pseudo-código ≤20 linhas) cobrindo o núcleo desta sala.
2. Calcule ou estime **um** número com unidade (Hz, µV, ms, dB, κ, Big-O, etc.).
3. Escreva a honesty note em 2 frases.
4. Liste pré-requisitos cumpridos (`requires_rooms`) e o que desbloqueia a seguir.
