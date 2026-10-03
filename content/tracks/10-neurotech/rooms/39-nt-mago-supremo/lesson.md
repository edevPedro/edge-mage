# Desafio — Verificação Final de Evidências do Mago Supremo

## 1. Objetivo do Desafio
Executar a verificação programática final do pacote de evidências do percurso de Neurotech e protocolar o ritual do Mago Supremo no diretório de artefatos.

## 2. Especificação Técnica e Formulação
Implemente a função `verify_supremo_pack(evidence_pack)` que verifica se o dicionário de evidências contém cumulativamente:
1. `evidence_pack.get("mago_base") is True`
2. `evidence_pack.get("neuro_mage") is True`
3. Todas as runas presentes: `{"acq", "decode", "online", "research"}.issubset(set(evidence_pack.get("runes", [])))`
4. `evidence_pack.get("paper_module_msc") is True`
5. `evidence_pack.get("ethics_limits_declared") is True`

Retorne uma tupla `(True, "Mago Supremo homologado com louvor")` se todas as condições forem rigorosamente satisfeitas, ou `(False, "Requisitos pendentes: ...")` caso contrário.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de criar o artefato `study-log/artifacts/neuro-supremo.md` com a declaração de síntese da jornada de especialização.
- Lembre-se: o Mago Supremo é o selo definitivo de que você dominou a neurotecnologia da biofísica ao firmware determinístico.
