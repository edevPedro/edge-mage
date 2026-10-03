# Desafio — Auditoria de Sequência Contígua Máxima (Max Streak)

## 1. Objetivo do Desafio
Implementar a rotina de auditoria de sequências de ensaios experimentais para detectar repetições excessivas da mesma classe (streaks) que comprometam a pseudoaleatorização do protocolo.

## 2. Especificação Técnica e Formulação
Dada uma lista de rótulos de classes inteiras ou strings `labels` representando a sequência cronológica de ensaios de uma sessão experimental:
- Implemente a função `max_streak(labels)` que retorna o comprimento da maior sequência contígua de elementos idênticos consecutivos:
  $$\text{max\_streak} = \max \{ \text{tamanho de repetições consecutivas de } c \}$$
- Se a lista estiver vazia, retorne 0.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que alternâncias perfeitas (ex. `[0, 1, 0, 1]`) retornem streak máximo 1.
- Uma sequência como `[1, 1, 1, 0, 0]` deve retornar 3.
