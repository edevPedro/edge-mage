# Desafio — Implementação de Buffer Circular (RingBuffer)

## 1. Objetivo do Desafio
Construir uma estrutura de dados de RingBuffer de capacidade estática fixa para streaming contínuo de amostras de EEG, garantindo armazenamento determinístico sem alocação dinâmica.

## 2. Especificação Técnica e Formulação
Implemente a classe `RingBuffer(capacity)` com os seguintes métodos:
1. `__init__(self, capacity)`: Inicializa o buffer interno com tamanho máximo fixo e contador de elementos.
2. `push(self, value)`: Insere uma nova amostra. Se o buffer atingir a capacidade máxima, o elemento mais antigo é descartado para dar lugar ao novo valor.
3. `is_full(self)`: Retorna `True` se o número de elementos contidos for igual à capacidade máxima, e `False` caso contrário.
4. `get_all(self)`: Retorna uma lista com todas as amostras atualmente armazenadas na ordem cronológica de inserção (da mais antiga para a mais recente).

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que a ordem temporal das amostras seja estritamente preservada ao recuperar os elementos via `get_all()`.
- Garanta que operações consecutivas de `push` além da capacidade não quebrem a estrutura nem acumulem vazamento de memória.
