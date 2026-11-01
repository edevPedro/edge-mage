# Desafio — Scheduler de batching contínuo (simulação em ticks)

## 1. Objetivo do Desafio
Simular um scheduler de *continuous batching* em ticks discretos e medir a
vazão, para entender por que slots poucos (mas dinâmicos) vencem o batch
estático.

## 2. Especificação Técnica e Formulação
- `continuous_batching_sim(requests, slots)`:
  - `request = (arrival_tick, n_tokens_to_generate)`.
  - A cada tick: enfileira as recém-chegadas (FIFO); termina requisições cujo
    `n_tokens` foi atingido; cada slot livre gera **1 token** para a próxima
    requisição da fila (mesma requisição pode continuar no slot no tick
    seguinte).
  - Retorna `(finished, total_tokens_generated)`.
- `batch_tokens_per_sec(requests, slots, max_tokens_each)`: rode a mesma
  simulação e retorne `total_tokens / makespan_ticks`, com `makespan_ticks` =
  tick do último token gerado (o tick 0 é o primeiro em que algo gera).

## 3. Critérios de Validação e Armadilhas
- Um slot só pode trabalhar em **uma** requisição por tick e meia; chão
  FIFO garante prioridade de chegada mais antiga.
- Total de tokens = soma dos `n_tokens` de todas as requisições.
- O teste de vazão: 2 requisições, 4 tokens cada, 2 slots → 8 tokens em 4 ticks
  (2 tokens/tick) → 2 tokens/s.
- Duplicatas na fila (mesma requisição) não podem ser agendadas em 2 slots
  simultaneamente.