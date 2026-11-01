# Lição — NEON na Prática

## Exercício 1: Dot Product em Lanes

Implemente mentalmente dot product de dois vetores de 8 floats:

```c
float dot_neon(const float* a, const float* b) {
    // 8 floats = 2 loads de float32x4_t cada
    float32x4_t va0 = vld1q_f32(a);
    float32x4_t va1 = vld1q_f32(a + 4);
    float32x4_t vb0 = vld1q_f32(b);
    float32x4_t vb1 = vld1q_f32(b + 4);
    
    // Multiplica elemento a elemento
    float32x4_t prod0 = vmulq_f32(va0, vb0);
    float32x4_t prod1 = vmulq_f32(va1, vb1);
    
    // Soma os dois vetores de produtos
    float32x4_t sum4 = vaddq_f32(prod0, prod1);
    
    // Redução horizontal: soma os 4 lanes
    return vaddvq_f32(sum4);
}
```

**Pergunta:** Quantas operações SIMD vs escalar? (Resposta: 2 vmul + 1 vadd + 1 vaddv vs 8 mul + 7 add)

## Exercício 2: Identificar Falha de Autovec

Por que este código **não** vetoriza?

```c
int sum = 0;
for (int i = 0; i < n; i++) {
    sum += arr[i];  // Loop-carried dependency em sum
}
```

**Solução:** Acumular em múltiplas variáveis independentes:

```c
int s0=0, s1=0, s2=0, s3=0;
for (int i = 0; i < n; i += 4) {
    s0 += arr[i]; s1 += arr[i+1]; s2 += arr[i+2]; s3 += arr[i+3];
}
int sum = s0 + s1 + s2 + s3;
```

## Exercício 3: Verificar no Godbolt

1. Vá em [godbolt.org](https://godbolt.org/)
2. Selecione `aarch64` com `-O3`
3. Compile:
   ```c
   void scale(float* arr, float factor, int n) {
       for (int i = 0; i < n; i++) arr[i] *= factor;
   }
   ```
4. Procure instruções NEON: `fmul v`, `ld1`, `st1`
5. Adicione `__restrict` ao ponteiro e compare

## Checklist: Quando Autovec Falha

| Problema | Solução |
|----------|---------|
| Aliasing | `__restrict` ou intrinsics |
| Loop-carried dep | Unroll manual, múltiplos acumuladores |
| Branch no loop | Predicação ou reestruturar |
| Stride irregular | Layout SoA ou gather manual |
| Tamanho desconhecido | Versão escalar para cleanup |

## Reflexão

Para o Forge F1 (NEON):
1. Qual operação do seu kernel é mais paralela?
2. O loop interno tem dependências?
3. O acesso a memória é contíguo (stride-1)?

Se as respostas são favoráveis, NEON pode dar 4× (f32) ou 16× (i8). Se não, reveja o algoritmo primeiro.

