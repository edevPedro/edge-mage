# Conceito — O Marco Integrador: Neuro Mage e Auditoria de Pipeline

O marco de **Neuro Mage** representa a primeira grande certificação de competência no percurso de neuroengenharia, consolidando o domínio de todo o ciclo de vida de uma Interface Cérebro-Computador não-invasiva.

## 1. Critérios Formais de Concessão do Neuro Mage
Para conquistar a consagração e a runa intermediária, o engenheiro deve comprovar:
1. **Domínio das Fases Fundamentais:** Conclusão bem-sucedida das salas de ética, matemática vetorial/matricial, física eletrostática, circuitos elétricos, neurociência de ritmos e estruturas de dados de streaming.
2. **Pipeline de Ponta a Ponta Operante:** Execução do loop online (`nt-online-stub`) com log de eventos comprovando conformidade com o orçamento de latência ($t_{\text{total}} < t_{\text{deadline}}$).
3. **Evidência Documentada:** Pelo menos um artefato formal validado em `study-log/artifacts/` (o Checkpoint de Paper OU o Checkpoint de Projeto — ambos caminhos paralelos válidos).
4. **Métricas Não-Viesadas:** Demonstração de que o classificador supera o nível de acaso através de Cohen's Kappa ($\kappa > 0$).

## 2. A Função de Auditoria de Pipeline
O código de auditoria (`audit_pipeline_evidence`) valida automaticamente se o dicionário de evidências contém todos os elos essenciais:
- Presença de dados (sintéticos ou benchmark público).
- Pré-processamento com filtro passa-faixa declarado.
- Modelo de decodificação ajustado com regularização.
- Métrica Kappa acima do limiar de acaso.
- Latência total compatível com o deadline de tempo real.

## 3. Modos de Falha na Auditoria
1. **Pipeline Incompleto:** Submeter evidências onde a latência foi omitida ou onde os filtros foram aplicados de forma não-causal.
2. **Alegações Clínicas Sem Base:** Incluir afirmações de uso diagnóstico em humanos em um pipeline puramente educacional de laboratório.

## 4. O que a Próxima Sala Assume
A próxima fase (`nt-stats-bci`) inicia aprofundamento em estatística inferencial, testes de permutação, cálculo de poder experimental e controle de falsos positivos.

## 5. Ponto de Destrave do Lab
Consulte as diretrizes de avaliação e maturidade técnica de pipelines de BCI em [Wolpaw & Wolpaw (Brain-Computer Interfaces: Principles and Practice, Oxford University Press)](https://global.oup.com/academic/product/brain-computer-interfaces-9780195388855).
