# Desafio — Atualização Sináptica por Regra Hebbiana

## 1. Objetivo do Desafio
Implementar a regra elementar de plasticidade sináptica associativa de Hebb, computando o ajuste linear do peso de conexão a partir dos níveis de atividade pré e pós-sináptica.

## 2. Especificação Técnica
Implemente a função `hebbian_update(w, pre, post, lr=0.01)`:
- Calcule a atualização aditiva do peso sináptico:
  $$w_{new} = w + \text{lr} \cdot \text{pre} \cdot \text{post}$$
- Onde:
  - `w`: Peso sináptico inicial (float).
  - `pre`: Sinal de ativação pré-sináptico (float).
  - `post`: Sinal de ativação pós-sináptico (float).
  - `lr`: Taxa de aprendizado (*learning rate*, float, padrão 0.01).

## 3. Critérios de Validação e Armadilhas
- Certifique-se de retornar um valor numérico float preciso.
- Entenda que essa formulação sem saturação cresceria ilimitadamente na biologia real, exigindo mecanismos homeostáticos ou termos de decaimento (como a regra BCM ou regras de Oja).
