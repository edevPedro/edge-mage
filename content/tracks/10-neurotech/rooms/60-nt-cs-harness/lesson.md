# Desafio — Detector de Perda de Pacotes por Sequenciamento

## 1. Objetivo do Desafio
Implementar a rotina de auditoria de integridade de transporte de pacotes eletrofisiológicos, calculando com precisão o número total de pacotes perdidos a partir de uma série temporal de identificadores de sequência sujeitos a estouro de contador (*wrap-around* modular).

## 2. Especificação Técnica
Implemente a função `detect_drops(seqs, max_seq=256)`:
- Receba uma lista de inteiros `seqs` contendo a sequência recebida de números de pacote.
- Se a lista contiver menos de 2 elementos, retorne `0`.
- Para cada par consecutivo de elementos $(s_i, s_{i+1})$:
  - Calcule o avanço modular:
    $$\Delta = (s_{i+1} - s_i) \pmod{max\_seq}$$
  - Se $\Delta > 1$, acumule $(\Delta - 1)$ pacotes perdidos.
- Retorne o número total acumulado de pacotes perdidos (inteiro).

## 3. Casos de Teste de Referência
- `detect_drops([0, 1, 2, 3])` $	o$ `0` (sequência contínua).
- `detect_drops([0, 2, 3])` $	o$ `1` (o pacote 1 foi perdido).
- `detect_drops([255, 1], max_seq=256)` $	o$ `1` (o contador deu a volta e o pacote 0 foi perdido).

## 4. Critérios de Validação e Armadilhas
- Certifique-se de aplicar a operação módulo `max_seq` corretamente em linguagens ou ambientes onde diferenças negativas possam ocorrer.
