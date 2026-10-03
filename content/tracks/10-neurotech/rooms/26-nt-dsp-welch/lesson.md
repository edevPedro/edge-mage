# Lição — Welch / vazamento

## Parâmetros

- `nperseg` / duração do segmento → Δf
- `noverlap` → estabilidade vs independência
- janela Hann/Hamming reduz vazamento

## Em lab

`synth_eeg_stream` + band-energy probes; **não** reivindique fisiologia.

Para destravar o lab, abra [scipy.signal.welch](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html) e leia os parâmetros nperseg e a média de segmentos na documentação de scipy.signal.welch, para welch_average e o Δf ≈ 1/T.

## Lab estendido (obrigatório no Estuda)

1. Produza um artefato (tabela, diagrama ASCII ou pseudo-código ≤20 linhas) cobrindo o núcleo desta sala.
2. Calcule ou estime **um** número com unidade (Hz, µV, ms, dB, κ, Big-O, etc.).
3. Escreva a honesty note em 2 frases.
4. Liste pré-requisitos cumpridos (`requires_rooms`) e o que desbloqueia a seguir.
