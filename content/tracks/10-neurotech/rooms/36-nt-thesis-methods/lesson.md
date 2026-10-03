# Desafio — Validação Computacional da Seção de Métodos

## 1. Objetivo do Desafio
Implementar a rotina de validação e verificação de integridade da especificação de Métodos científicos e protocolar o artefato correspondente em `study-log/artifacts/neuro-thesis-methods.md`.

## 2. Especificação Técnica e Formulação
Implemente a função `validate_methods_spec(spec_text)` que recebe um texto em formato de checklist estruturado em YAML/markdown e verifica se todos os campos obrigatórios estão preenchidos:
1. `data`: identificador do dataset e população.
2. `preprocessing`: especificação detalhada de filtros e frequências.
3. `features_model`: formulação do extrator de features e classificador.
4. `validation`: protocolo de validação cruzada sem vazamento de dados.
5. `seeds_versions`: versões de bibliotecas e semente aleatória.
6. `limits`: declaração explícita de pesquisa educacional e limites biofísicos.

A função deve retornar `(True, "Especificação válida e completa")` se todos os campos forem preenchidos, ou `(False, "Campos faltantes: ...")` caso contrário.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de preencher o artefato `study-log/artifacts/neuro-thesis-methods.md` com todos os 6 campos obrigatórios.
- A ausência de qualquer um dos campos invalida a submissão do ritual.
