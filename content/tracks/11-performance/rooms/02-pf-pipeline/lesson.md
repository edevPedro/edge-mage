# Lição — Pipeline na Prática

## Exercício Mental: Analisando Dependências

Considere o código abaixo. Identifique as dependências:

```asm
; AArch64
ldr  x1, [x0]       ; i1: load
add  x2, x1, #5     ; i2: usa x1 (RAW com i1)
mul  x3, x2, x4     ; i3: usa x2 (RAW com i2)
str  x3, [x5]       ; i4: usa x3 (RAW com i3)
```

**Cadeia crítica:** i1 → i2 → i3 → i4. Mesmo com OoO, esta sequência serializa.

## Checklist de Análise

1. **Distinga hazard de data vs controle:**
   - Data: operando não está pronto (RAW mais comum)
   - Control: não sabemos o próximo PC (branch)

2. **Forwarding não resolve tudo:**
   - Load-use: dado só está disponível após MEM, não após EX
   - Resultado: 1 ciclo de stall inevitável em `ldr x1; add x2, x1, ...`

3. **ILP em kernels:**
   - Densos (GEMM): muito trabalho por dado → esconde latência
   - Esparsos (pointer-chasing): cada load depende do anterior → baixo ILP

## Experimento: Godbolt

1. Vá em [godbolt.org](https://godbolt.org/)
2. Compile para `aarch64` com `-O3`:
   ```c
   int sum_chain(int* arr, int n) {
       int s = 0;
       for (int i = 0; i < n; i++) s += arr[i];
       return s;
   }
   ```
3. Observe: o compilador **não** consegue vetorizar devido à dependência loop-carried no acumulador
4. Compare com versão que acumula em 4 variáveis separadas

## Reflexão

Antes da próxima sala (cache), responda:
- Seu kernel tem cadeia longa de dependências?
- Há independência suficiente para o processador superscalar?
- O limite é pipeline (ILP) ou memória (bandwidth)?

