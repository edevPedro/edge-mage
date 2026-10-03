# Desafio — Integrador Probabilístico com Dwell Accumulator

## 1. Objetivo do Desafio
Implementar um integrador de evidência temporal (*dwell accumulator*) que processa um fluxo contínuo de probabilidades de decodificação neural, acumulando a evidência passo a passo até atingir ou ultrapassar o limiar de decisão estipulado.

## 2. Especificação Técnica
Implemente a função `dwell_accumulate(prob_stream, threshold=3.0)`:
- Receba uma lista ou iterável de probabilidades de ponto flutuante `prob_stream`.
- Mantenha um somatório acumulado inicializado em `0.0`.
- Percorra a sequência de probabilidades amostra a amostra:
  - Adicione a probabilidade atual ao somatório acumulado.
  - Se o somatório acumulado for maior ou igual ao `threshold`, retorne imediatamente o número de passos decorridos (1-indexado, ou seja, a quantidade de amostras processadas até o disparo).
- Se a sequência terminar sem atingir o limiar, retorne o total de amostras da lista (ou o comprimento processado).

## 3. Exemplo de Validação
```python
probs = [0.5, 0.8, 0.9, 0.9]
# Passo 1: soma = 0.5
# Passo 2: soma = 0.5 + 0.8 = 1.3
# Passo 3: soma = 1.3 + 0.9 = 2.2
# Passo 4: soma = 2.2 + 0.9 = 3.1 >= 3.0 -> Dispara no passo 4!
assert dwell_accumulate(probs, threshold=3.0) == 4
```

## 4. Critérios de Validação e Armadilhas
- Certifique-se de retornar um número inteiro representando o número exato de amostras avaliadas até a condição de disparo.
