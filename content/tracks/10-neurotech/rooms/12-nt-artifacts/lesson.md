# Lição — Artefatos no pipeline

1. Nomeie fontes: EOG, EMG, movimento, linha 50/60 Hz.
2. Separe *detecção/rejeição* de trial vs *robustez* do modelo.
3. Micro-exemplo: `artifact_inject` com `kind=line` eleva potência ~60 Hz — compare com `detect_line_power`.
4. Em MI, rejeitar trials com blink extremo é comum; fingir que não existem não é.
5. Estuda → Sala: rode `mage emu artifact` antes de culpar o classificador.

Para destravar o lab, abra [Urigüen & Garcia-Zapirain — EEG artifact removal methods (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4462641/) e leia a taxonomia de remoção de artefato de Urigüen (EOG, EMG, linha) para decidir o limiar de flag_artifacts em vez de chamar o pico de ritmo.

## Lab estendido (obrigatório no Estuda)

1. Produza um artefato (tabela, diagrama ASCII ou pseudo-código ≤20 linhas) cobrindo o núcleo desta sala.
2. Calcule ou estime **um** número com unidade (Hz, µV, ms, dB, κ, Big-O, etc.).
3. Escreva a honesty note em 2 frases.
4. Liste pré-requisitos cumpridos (`requires_rooms`) e o que desbloqueia a seguir.
