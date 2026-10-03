# Desafio — Implementação de Filtro Biquad IIR e Projeto Butterworth

## 1. Objetivo do Desafio
Implementar a execução amostra a amostra de uma seção de segunda ordem (Biquad IIR) em Direct Form II Transposed e calcular coeficientes analíticos de um filtro passa-baixas Butterworth de 2ª ordem.

## 2. Especificação Técnica e Formulação
1. **Passo de Biquad:** Implemente `biquad_step(x, state, b, a)` onde:
   - `state` é uma lista de dois elementos flutuantes `[w1, w2]`.
   - `b` tem coeficientes `[b0, b1, b2]` e `a` tem `[1.0, a1, a2]`.
   - Calcule a saída: $y = b_0 x + w_1$.
   - Atualize os estados: $w_1 = b_1 x - a_1 y + w_2$ e $w_2 = b_2 x - a_2 y$.
   - Retorne a tupla `(y, [w1, w2])`.
2. **Projeto Butterworth:** Implemente `design_butterworth_biquad(cutoff_hz, fs_hz)` utilizando a transformada bilinear com pré-distorção de frequência (frequency warping).

## 3. Critérios de Validação e Armadilhas
- Certifique-se de atualizar os estados internos na ordem correta para não sobrescrever $w_1$ antes de utilizá-lo no cálculo de $y$.
- O filtro deve ser estritamente estável (polos no interior do círculo unitário no plano z).
