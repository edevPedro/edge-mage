# Desafio — Execução e Avaliação de Pipeline Experimental

## 1. Objetivo do Desafio
Implementar a rotina integradora de avaliação experimental de pipeline e protocolar o artefato do projeto de pesquisa em `study-log/artifacts/research-project.md` para a conquista da Runa de Pesquisa.

## 2. Especificação Técnica e Formulação
Implemente a função `run_bci_pipeline_eval(data, labels, config)` que:
1. Recebe a matriz multicanal de dados e o vetor de rótulos.
2. Executa a filtragem conforme `config.get("filter_band", (8, 30))`.
3. Conduz a validação cruzada por blocos conforme `config.get("n_splits", 5)`.
4. Retorna um dicionário com os resultados:
   - `"accuracy"`: acurácia observada média ($0.0\text{ a } 1.0$).
   - `"cohen_kappa"`: coeficiente Kappa de Cohen médio.
   - `"mean_latency_ms"`: tempo médio de processamento por janela em milissegundos.
   - `"status"`: `"SUCCESS"` se $\kappa \ge 0.40$, ou `"FAIL"` caso contrário.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de que o artefato `study-log/artifacts/research-project.md` seja preenchido com a descrição completa dos resultados e a declaração da runa `rune-neuro-research`.
- O pipeline deve ser totalmente reproduzível com sementes fixadas.
