# Desafio — Particionamento em Blocos e Auditoria de Vazamento de Folds

## 1. Objetivo do Desafio
Implementar a rotina de particionamento de validação cruzada em blocos contíguos de ensaios e construir um auditor automático de vazamento de índices entre conjuntos de treino e teste.

## 2. Especificação Técnica e Formulação
1. **Split em Blocos:** Implemente `split_blocked_cv(n_trials, n_blocks)`:
   - Divide $N$ ensaios em $K$ blocos temporais contíguos disjuntos.
   - Retorna uma lista de $K$ tuplas `(train_indices, test_indices)`, onde no $k$-ésimo fold, o $k$-ésimo bloco é o teste e os demais formam o treino.
2. **Auditoria de Vazamento:** Implemente `audit_leakage(train_idx, test_idx)`:
   - Verifica se a interseção de índices entre treino e teste é vazia: $\text{set}(\text{train}) \cap \text{set}(\text{test}) = \emptyset$.
   - Retorna uma tupla `(True, "Split limpo sem vazamento")` se não houver sobreposição, ou `(False, "Vazamento detectado: índices compartilhados")` caso contrário.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que a união de todos os conjuntos de teste cubra exatamente todos os ensaios originais de $0$ a $N-1$ sem repetições.
- Lembre-se: em ciência de dados biomédicos, o particionamento deve sempre respeitar a integridade de blocos temporais.
