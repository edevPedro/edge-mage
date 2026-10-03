# Lição — Boss Neuro Mage: Memorial de Engenharia e Auditoria de Pipeline

## 1. O Ritual do Neuro Mage
Para selar a sala do boss `nt-neuro-mage`, o estudante deve:
1. Concluir a tarefa de código `audit-neuro-mage-evidence`, implementando a função `audit_pipeline_integrity(evidence)` que valida a presença de filtro causal, Kappa estritamente positivo e latência de loop $<150\text{ ms}$.
2. Produzir o artefato `study-log/artifacts/neuro-mage.md` contendo:
   - Origem dos dados (`data` ou `data_source`).
   - Métrica primária (`primary_metric` ou `metrics`, com Kappa de Cohen).
   - Limites éticos e metodológicos declarados (`limits` ou `ethical_limits`).
   - Número do fundamento: latência medida (`latency_ms`) compatível com o deadline neurofisiológico.
   - Referência a módulo de paper ou fatia de projeto e evidência do loop online.

## 2. A Função de Laboratório
- `audit_pipeline_integrity(evidence)`: Recebe um dicionário com `has_filter`, `test_kappa` e `latency_ms`, auditando se todos os requisitos técnicos de integridade de malha fechada estão cumpridos.

Para destravar o lab, abra [SPEC Neurotech](https://github.com/edevPedro/edge-mage/blob/main/docs/SPEC-neurotech-course.md) e leia as runas e os gates do SPEC (o que o rank exige em artefato e latência numérica) para fechar o ritual do Neuro Mage.
