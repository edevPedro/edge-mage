# Conceito — O Miniprojeto de Pesquisa Experimental e a Runa de Pesquisa

O miniprojeto de pesquisa quantitativa consolida a capacidade do pesquisador de conduzir uma investigação experimental completa, desde os dados brutos até as métricas finais auditadas.

## 1. O Ciclo Completo de Execução Experimental
O miniprojeto deve executar programaticamente:
```text
Dados Brutos (Open Dataset / Synth) 
   → Pré-Processamento Causal (Passa-Faixa + Notch)
   → Fatiamento Temporal de Ensaios (Epoch Slicing)
   → Validação Cruzada por Blocos (Sem Vazamento)
   → Extração de Características Espaciais (CSP / Riemann / Bandpower)
   → Ajuste de Classificador Regularizado (LDA / Shrinkage)
   → Predição em Teste Independente
   → Cálculo de Métricas (Acurácia, Kappa de Cohen e Latência)
```

## 2. A Runa de Pesquisa (`rune-neuro-research`)
A conclusão bem-sucedida do ritual e a validação do artefato em `study-log/artifacts/research-project.md` confere ao estudante a cobiçada **Runa de Pesquisa Neural** (`rune-neuro-research`), requisito mandatório para a elegibilidade ao Boss final Mago Supremo pela rota de Neurotech.

## 3. Modos de Falha no Miniprojeto
1. **Regressão de Métricas:** Apresentar acurácia média compatível com o nível de acaso ($\kappa < 0.20$), indicando que o filtro ou o extrator espacial foi mal configurado.
2. **Inconsistência de Dimensões:** Falha de compatibilidade de canais entre o conjunto de treino e o conjunto de teste.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-paper-module-msc`) exige a formatação dos resultados experimentais em um módulo de artigo científico completo com DOI e discussão crítica de limitações.

## 5. Ponto de Destrave do Lab
Consulte os benchmarks públicos e pipelines de referência do [BCI Competition IV Dataset 2a](https://www.bbci.de/competition/iv/) e o framework [MOABB (Mother of all BCI Benchmarks)](https://github.com/NeuroTechX/moabb).
