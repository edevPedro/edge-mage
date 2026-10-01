# Conceito — AArch64 ABI (edge)

## AAPCS64 (fonte: abi-aa)
- Args inteiros/ponteiros: **x0–x7**; depois stack.
- Retorno escalar típico: **x0/w0**; resultado indireto: **x8**.
- **SP** alinhado a **16 bytes** na interface pública.
- Callee-saved GPR: **x19–x28**; frame/link: **x29/x30** quando usados como FP/LR.

## Advanced SIMD (NEON)
Vetor 128-bit → **16×int8** (ou 8×int16, 4×f32, …). Kernels quantizados contam lanes.

## Manual de arquitetura
DDI0487 (Arm ARM A-profile) é a referência de instruções A64 / Advanced SIMD — não um tutorial.
