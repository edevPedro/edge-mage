# Lição — Stream sintético + ring buffer

```bash
mage emu synth   # µV didáticos; mu_burst = band-energy probe
mage emu cortex  # Python host stub (não QEMU)
```

1. Mode: **simulated online** — `tick()` / chunks, não dataset inteiro.
2. Implemente ring buffer testável (capacidade fixa, push, latest).
3. Micro-exemplo: fs=250, janela 128 amostras ≈ 512 ms de sense — compare com deadline depois.
4. Unidades do synth: µV didáticos (não calibração clínica).
5. Sala: complete o `RingBuffer` na tarefa de código.

## Fontes
- SPEC Neurotech §5 emuladores
