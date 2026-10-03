# Conceito — Mini-Projeto de Pesquisa Experimental: Conexão Fim-a-Fim e Runa de Pesquisa

## 1. O Projeto de Engenharia Neural Aplicada
O mini-projeto de pesquisa consolida a transição do estudante de um mero consumidor de bibliotecas para um pesquisador em neuroengenharia capaz de conceber, executar e auditar um pipeline experimental completo.

Concluir este ritual materializa a quarta e última runa fundamental do catálogo: **`rune-neuro-research`**.

### Os Requisitos Formais do Artefato (`study-log/artifacts/neuro-research-project.md`)
O relatório de execução experimental deve conter os quatro parâmetros obrigatórios auditados pelo sistema:
1. **Dados (`data`)**: Identificação clara da base de dados utilizada (ex: ensaios sintéticos com SNR controlada gerados pelo emulador `online_loop` ou gravações abertas do BCI Competition IV 2a).
2. **Métricas (`metrics`)**: Tabela quantitativa contendo acurácia observada ($p_o$), coeficiente Kappa de Cohen ($\kappa$) e matriz de confusão $2 \times 2$.
3. **Limites e Salvaguardas Éticas (`limits`)**: Declaração explícita de que os testes foram conduzidos em ambiente de bancada sem finalidade clínica intervencionista e com adesão às diretrizes de privacidade de neurodados.
4. **Número do Fundamento Físico/Computacional**: Parâmetro com unidade derivada da física da aquisição (ex: $\text{SNR} = 18.5\text{ dB}$, $\gamma_{\text{shrinkage}} = 0.1$, latência de processamento $T_{\text{pipeline}} = 38.0\text{ ms}$).
5. **Evidência de Execução (`code_or_log`)**: Trecho de código ou log determinístico da execução com o sumário dos resultados (`results_summary`).

## 2. Modos de Falha Operacionais
1. **Apresentar Acurácia sem Matriz de Confusão ou Kappa**: Submeter um mini-projeto que apenas exibe "acurácia média de $83\%$" sem reportar a distribuição dos erros por classe. A matriz de confusão e o Kappa são indispensáveis para comprovar que o modelo não sofre de viés assimétrico em favor de uma das classes.
2. **Executar Pipeline sem Validação Independente**: Treinar os pesos $\mathbf{w}$ em todo o conjunto e testar no mesmo conjunto. O pipeline deve executar divisão contígua em blocos disjuntos (ex: $67\%$ treino, $33\%$ teste).

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-paper-module-msc`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/38-nt-paper-module-msc/room.yaml)) assume que você possui a runa de pesquisa (`rune-neuro-research`) e exige a redação de um módulo crítico de paper reproduzindo formalmente uma publicação internacional indexada com DOI oficial.
