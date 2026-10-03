# Lição — Latência closed-loop

1. Liste sense / decide / act com ms estimados.
2. `mage emu cortex` — deadline padrão 40 ms; janela de 32 amostras @ 250 Hz **deve** miss (window-dominated).
3. Micro-exemplo: encurtar janela reduz sense, mas piora SNR de feature — trade-off.
4. Animação `closed_loop_timeline`.
5. Documente misses no artefato online depois.

## Fontes
- [Alzahab et al. MDPI](https://www.mdpi.com/1424-8220/21/6/2173) (desafios online)
