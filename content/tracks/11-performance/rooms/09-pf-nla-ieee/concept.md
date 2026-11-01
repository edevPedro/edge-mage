# Conceito — NLA e IEEE 754

IEEE 754 define formatos binários, arredondamentos, NaN/Inf e exceções. Em performance engineering, o ponto crítico é: **otimização sem prova numérica é teatro**.

## Associatividade quebrada

Em float, `(a+b)+c` pode diferir de `a+(b+c)`. Reduções vetoriais, reassociação do compilador e `fast-math` mudam bits. Por isso todo Performance Boss declara **tolerância** (abs/rel ou ULP) contra um golden.

## NLA prática neste curso

O suficiente para operar:

- Normas e erros (RMS, max abs).
- Matmul / GEMM como kernel denso.
- Jacobi / difusão como stencil iterativo.

Não substituímos um curso completo de análise numérica; amarramos estabilidade ao harness.

## Flags

Documente `-ffast-math`, FMA, e precisão (`f32`/`f64`) no artefato. Comparar benches com flags diferentes sem nota é autoengano.
