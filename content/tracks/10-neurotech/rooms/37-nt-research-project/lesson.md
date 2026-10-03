# Lição — Mini-Projeto de Pesquisa Experimental

## 1. A Estrutura do Pipeline Experimental
1. **Partição em Blocos**:
   Dividir o conjunto de ensaios em treino ($67\%$) e teste ($33\%$) contíguos sem permutação aleatória.
2. **Estimação com Regularização**:
   Calcular a matriz de dispersão intra-classes combinada e aplicar regularização de shrinkage ($\gamma = 0.1$) para garantir estabilidade numérica.
3. **Avaliação Fim-a-Fim**:
   Predizer o conjunto de teste, extrair a matriz de confusão, calcular acurácia observada e coeficiente Kappa de Cohen.
4. **Memorial de Engenharia**:
   Redigir o relatório estruturado em `study-log/artifacts/neuro-research-project.md` cumprindo os quatro pilares quantitativos.

## 2. A Função de Laboratório
- `run_bci_pipeline(X_trials, y_labels)`: Executa a pipeline experimental completa em Python, retornando o dicionário com acurácia, Kappa de Cohen e matriz de confusão.

Para destravar o lab, abra [Lotte et al. classification review](https://doi.org/10.1088/1741-2560/4/2/R01) e leia o que Lotte exige de um pipeline de classificação (estágios e validação) para o projeto reportar métrica com limite, não um número solto.
