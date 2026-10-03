# Desafio — Parser Topográfico do Sistema 10–20

## 1. Objetivo do Desafio
Implementar um analisador determinístico da nomenclatura do sistema internacional de eletrodos 10-20, classificando a lateralidade anatômica (hemisfério esquerdo, direito ou linha média) a partir do identificador alfanumérico do canal.

## 2. Especificação Técnica
Implemente a função `channel_hemisphere(ch_name)`:
- Avalie o sufixo ou último caractere da string `ch_name` (insensível a maiúsculas/minúsculas):
  - Se terminar com a letra `'z'` ou `'Z'`, retorne `'midline'`.
  - Se terminar com um dígito numérico ímpar (`1, 3, 5, 7, 9`), retorne `'left'`.
  - Se terminar com um dígito numérico par (`0, 2, 4, 6, 8`), retorne `'right'`.
- Exemplos:
  - `channel_hemisphere("C3")` $	o$ `'left'`
  - `channel_hemisphere("C4")` $	o$ `'right'`
  - `channel_hemisphere("Cz")` $	o$ `'midline'`
  - `channel_hemisphere("Fp2")` $	o$ `'right'`

## 3. Critérios de Validação e Armadilhas
- Certifique-se de manipular nomes de eletrodos compostos como "Fp1" e "Fp2" inspecionando corretamente o último caractere da string.
- O resultado deve ser retornado em letras minúsculas exatamente conforme especificado.
