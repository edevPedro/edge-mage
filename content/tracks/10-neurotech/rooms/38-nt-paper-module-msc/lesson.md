# Desafio — Verificação Quantitativa de Reprodução de Artigo MSc

## 1. Objetivo do Desafio
Implementar a rotina de validação quantitativa de reprodução de métricas de artigo científico e protocolar o artefato do módulo de mestrado em `study-log/artifacts/neuro-paper-module-msc.md`.

## 2. Especificação Técnica e Formulação
Implemente a função `verify_paper_reproduction(paper_meta, observed_metrics, tolerance=0.15)` que:
1. Extrai o DOI permanente de `paper_meta.get("doi")`.
2. Compara a acurácia observada `observed_metrics["accuracy"]` contra `paper_meta["reported_accuracy"]`.
3. Compara o Kappa observado `observed_metrics["cohen_kappa"]` contra `paper_meta["reported_kappa"]`.
4. Verifica se ambos os desvios relativos estão dentro do limiar de tolerância:
   $$\frac{|\text{obs} - \text{rep}|}{\text{rep}} \le \text{tolerance}$$
5. Retorna uma tupla `(True, "Reprodução consistente dentro da tolerância")` em caso positivo, ou `(False, "Desvio excessivo em relação ao artigo")` caso contrário.

## 3. Critérios de Validação e Armadilhas
- Certifique-se de preencher o artefato `study-log/artifacts/neuro-paper-module-msc.md` com o DOI oficial do estudo replicado e as métricas observadas.
- A tolerância acomoda variações estocásticas normais, mas desvios superiores a 15% indicam divergências de pré-processamento.
