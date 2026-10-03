# Desafio — Produto Escalar Vetorizado SIMD-4

## 1. Objetivo do Desafio
Implementar a simulação algorítmica de uma instrução vetorial SIMD de 4 vias (como o bloco fundamental das instruções Neon da arquitetura ARM AArch64), calculando o produto escalar de dois vetores de 4 elementos.

## 2. Especificação Técnica
Implemente a função `simd4_dot(a, b)`:
- Receba dois vetores iteráveis `a` e `b`, cada um contendo exatamente 4 elementos de ponto flutuante.
- Calcule o produto escalar elemento a elemento:
  $$\text{dot} = \sum_{i=0}^3 a[i] \times b[i] = a[0]b[0] + a[1]b[1] + a[2]b[2] + a[3]b[3]$$
- Retorne o valor escalar float resultante.

## 3. Exemplo de Validação
```python
a = [1.0, 2.0, 3.0, 4.0]
b = [2.0, 0.0, 1.0, -1.0]
# 1*2 + 2*0 + 3*1 + 4*(-1) = 2 + 0 + 3 - 4 = 1.0
assert abs(simd4_dot(a, b) - 1.0) < 1e-5
```

## 4. Critérios de Validação e Armadilhas
- Certifique-se de manipular com precisão números negativos e produtos nulos.
- O resultado deve ser um valor numérico escalar único (float).
