# Desafio — O loop de geração e suas métricas

## 1. Objetivo do Desafio
Implementar a escolha greedy do próximo token e as duas métricas que resumem o
decode: vazão (tokens/s) e latência inter-token (ITL).

## 2. Especificação Técnica e Formulação
- `greedy_argmax(logits)` → índice do maior valor (empate → primeiro índice).
- `tokens_per_second(n_tokens, elapsed_s)` → `n_tokens / elapsed_s`.
- `inter_token_latency_s(n_new_tokens, elapsed_s)` → `elapsed_s / n_new_tokens`.

## 3. Critérios de Validação e Armadilhas
- `argmax` deve retornar o *índice*, não o valor.
- Com `elapsed_s == 0`, divisões devem ser tratadas (retorne `0.0` para
  tokens/s e `0.0` para ITL).
- Note a relação: `ITL = 1 / tokens_per_second` (recíprocos), e lembre que na
  prática o decode é bound por memória, não por FLOPs.