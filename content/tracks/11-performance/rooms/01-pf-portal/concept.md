# Conceito — Performance Mage como especialização

Performance Mage **não** substitui Fundamentals, Systems nem Edge ML. É uma **especialização** sobre o fundamento da academia e-mage: medir, explicar e provar.

## Mapa dos pilares (12 meses aspiracionais)

| Fase | Pilares | Entrega típica |
|------|---------|----------------|
| M1–2 | Arquitetura & memória (pipeline, cache, TLB, ABI) | Modelar bottleneck de memória vs compute |
| M3–4 | ARM Performance (NEON/SIMD, tiling, counters) | Biblioteca math vetorizada + medição |
| M5–6 | Numerical / HPC (IEEE754, Roofline, GEMM) | Simulação física correta + Roofline |
| M7–8 | GPU (Metal first; CUDA eletiva) | Kernels Metal com evidência |
| M9–10 | Inference bridge (soft → Edge ML) | Literacy ORT/CoreML/llama.cpp — **não** gate Edge |
| M11–12 | HW/SW co-design (RTL/HLS lite) | Acelerador pedagógico |

Faixa aspiracional de especialização: **~310–415 h** a 6–8 h/semana. Este scaffold entrega salas densas nos pilares; horas reais sobem com labs de medição no seu Mac/SoC.

## Pedagogia

```text
Estuda (story + concept + lesson) → Sala (tasks curtas) → Projeto/Boss (2 versões + medida + prova)
```

## Caveats Apple Silicon (M4 e família)

1. **µarch ≠ Cortex-A**: timings e contadores de um M4 **não** transferem 1:1 para um Cortex-A78/X4.
2. **Sem SVE no M4**: foque NEON / ASIMD; SVE é literacy para servidores Arm, não lab nativo M4.
3. **Metal ≠ CUDA**: modelo de memória, tooling e ecossistema diferem; CUDA é eletiva/complemento.

## Relação com Edge ML

Performance **não** é pré-requisito duro do caminho Edge / Mago Supremo. Soft deps: salas avançadas de Edge (SIMD/quant kernels) *podem* apontar para salas Performance; o aluno Edge segue on-device sem zerar Performance.

