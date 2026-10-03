# Desafio — Regularização Numérica de Matriz (Carga Diagonal)

## 1. Objetivo do Desafio
Implementar a técnica de regularização por carga diagonal (*diagonal loading* / regularização de Tikhonov) em uma matriz quadrada, garantindo estabilidade numérica para operações subsequentes de inversão e decomposição espectral.

## 2. Especificação Técnica
Implemente a função `regularize_matrix(mat, lambda_reg=1e-3)`:
- Receba uma matriz quadrada `mat` (lista de listas de tamanho $C \times C$ ou array bidimensional).
- Some o valor escalar `lambda_reg` a cada um dos elementos da diagonal principal ($mat[i][i]$ para $0 \le i < C$).
- Mantenha todos os elementos fora da diagonal rigorosamente inalterados.
- Retorne a nova matriz regularizada preservando as dimensões originais.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de não modificar a matriz original caso receba cópias por referência, retornando uma estrutura de dados consistente.
- A regularização deve incidir estritamente sobre a diagonal principal ($i == j$).
