# Desafio — Estrutura de Dados Ring Buffer com Política Overwrite

## 1. Objetivo do Desafio
Implementar uma classe `Ring` que gerencie um buffer circular de capacidade fixa pré-alocada, oferecendo operações de inserção com política de descarte do elemento mais antigo (*overwrite*) e recuperação instantânea do elemento mais recente.

## 2. Especificação Técnica
Crie a classe `Ring`:
- `__init__(self, capacity)`: Inicializa a estrutura para armazenar no máximo `capacity` elementos.
- `push(self, x)`: Insere o elemento `x`. Se a capacidade máxima já foi atingida, sobrescreve o elemento mais antigo mantendo a capacidade invariante.
- `latest(self)`: Retorna o último elemento escalar inserido na estrutura (o valor de `x` do `push` mais recente).

## 3. Exemplo de Comportamento
```python
r = Ring(3)
for v in [1, 2, 3, 4]:
    r.push(v)
assert r.latest() == 4
```

## 4. Critérios de Validação e Armadilhas
- Certifique-se de que `latest()` retorne o escalar correspondente ao último valor inserido, e não uma lista ou coleção.
- Não permita que a estrutura cresça indefinidamente além do limite estipulado em `capacity`.
