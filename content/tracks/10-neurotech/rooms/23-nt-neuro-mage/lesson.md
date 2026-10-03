# Desafio — Auditoria de Evidências do Marco Neuro Mage

## 1. Objetivo do Desafio
Implementar a rotina formal de auditoria de evidências de engenharia e protocolar o artefato do Boss Neuro Mage no repositório de estudos.

## 2. Especificação Técnica e Formulação
Implemente a função `audit_pipeline_evidence(evidence_dict)` que verifica se o dicionário de evidências satisfaz cumulativamente:
1. `evidence_dict.get("data")` é não-vazio.
2. `evidence_dict.get("filter")` é não-vazio (ex. "bandpass 8-30Hz").
3. `evidence_dict.get("model")` é não-vazio (ex. "LDA" ou "CSP+LDA").
4. `evidence_dict.get("kappa", 0.0) >= 0.40`.
5. `evidence_dict.get("latency_ms", 999.0) <= evidence_dict.get("deadline_ms", 150.0)`.

Retorne uma tupla `(True, "Evidências aprovadas")` se todos os critérios forem satisfeitos, ou `(False, "Motivo da falha")` caso contrário.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de criar o artefato `study-log/artifacts/neuro-mage-evidence.md` com a documentação do seu loop online e métricas.
- Lembre-se: o marco Neuro Mage coroa a integração de hardware, sinal e matemática.
