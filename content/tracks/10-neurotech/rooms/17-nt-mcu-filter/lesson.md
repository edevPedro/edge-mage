# Lição — Stub embutido

```bash
mage emu cortex
python -m edge_mage.emulators cortex
```

1. Pipeline: ADC → ring → FIR/MA stub → packet UART-like.
2. Observe `window_ms` vs `compute_ms` no relatório — a janela costuma dominar.
3. Micro-exemplo: 32 amostras @ 250 Hz → window 128 ms → miss se deadline=40 ms.
4. Não confunda com QEMU/CMSIS: aqui é pedagogia de orçamento no host Python.
5. Depois aprofunde kernels em Edge (`cmsis-nn`).

## Fontes
- [CMSIS-NN (Arm)](https://github.com/ARM-software/CMSIS-NN) — referência Edge, não runtime deste stub
