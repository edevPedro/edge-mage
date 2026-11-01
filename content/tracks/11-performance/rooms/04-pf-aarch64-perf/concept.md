# Conceito — AArch64 para performance

Systems Mage ensina a **ler** frames, `x0`–`x7`, stack. Performance pergunta: o kernel é *load/store bound*? Alinhamento e múltiplos de vetor importam?

## Pontos de pressão

- Loads/stores vs aritmética (intensidade aritmética → Roofline).
- Calling convention: spills excessivos matam ILP em hot loops — inline / Restrict / LTO ajudam quando medidos.
- **Apple Silicon**: decode/rename widths e caches diferem de Cortex-A; valide no **seu** chip.

## Compartilhamento com Systems

Não duplique o currículo Systems. Aqui aprofunda-se o ângulo de **medição** e preparação para NEON.

