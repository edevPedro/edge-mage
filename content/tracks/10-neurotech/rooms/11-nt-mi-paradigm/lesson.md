# Lição — Paradigma MI

## Objetivos

Desenhar um trial MI left/right com janelas claras; ligar a C3/C4 e ERD; declarar limites do synth.

## Passos

1. Esboce timeline: ITI → cue → MI (ex. 3–4 s) → rest.
2. Marque onde calcula bandpower (só MI? MI − baseline?).
3. Associe classes L/R a C3/C4 (contralateral).
4. Leia Pfurtscheller (DOI na sala): uma figura mental de ERD.
5. Escreva honesty: *synth ≠ ERD*.

## Labs

**Design.** 2 classes, 40 trials/classe, ITI ≥ 1 s. Qual o risco se todos os left vêm na 1ª metade da sessão?

**Numeric.** Se MI window = 2.0 s a `fs=250`, quantas amostras por trial por canal?

**Fill mental.** “ERD em MI significa tipicamente ___ de potência em mu/beta.” → *queda/redução*.

Para destravar o lab, abra [Padfield et al. EEG-MI (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) e leia uma figura de paradigma MI / ERD em Padfield para cravar pre e post do slice_epoch em torno do trigger, sem misturar com a sessão inteira.

## Lab estendido (obrigatório no Estuda)

1. Produza um artefato (tabela, diagrama ASCII ou pseudo-código ≤20 linhas) cobrindo o núcleo desta sala.
2. Calcule ou estime **um** número com unidade (Hz, µV, ms, dB, κ, Big-O, etc.).
3. Escreva a honesty note em 2 frases.
4. Liste pré-requisitos cumpridos (`requires_rooms`) e o que desbloqueia a seguir.
