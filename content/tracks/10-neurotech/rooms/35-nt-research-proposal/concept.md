# Conceito — Formulação de Proposta de Pesquisa Científica em BCI (MSc-Prep)

A proposta de pesquisa formal é o contrato acadêmico que estabelece a viabilidade, a metodologia e o rigor experimental de um projeto de pós-graduação.

## 1. Estrutura Canônica de uma Proposta de Pesquisa
Uma proposta técnica de alto nível deve articular com precisão:
1. **Declaração do Problema e Hipótese Científica:** Definição da lacuna de conhecimento e a previsão quantitativa a ser testada experimentalmente.
2. **Especificação dos Dados:** Nome do dataset aberto, identificador permanente (DOI/URL), número de participantes, canais de registro e montagem de referência.
3. **Pipeline Metodológico:** Filtros digitais de pré-processamento, algoritmos de extração de características e classificadores matemáticos com hiperparâmetros declarados.
4. **Métricas de Desempenho e Hipótese Nula:** Definição da métrica primária (Cohen's Kappa $\kappa$, ITR de Wolpaw) e o teste inferencial não-paramétrico (teste de permutação ou Wilcoxon pareado) para rejeição da hipótese nula com nível $\alpha = 0.05$.
5. **Declaração Ética e Limites:** Esclarecimento de que a pesquisa opera sobre dados de acesso aberto desidentificados, sem pretensões de diagnóstico clínico humano sem certificação regulatória.

## 2. O Papel do Artefato de Proposta
A criação do arquivo `study-log/artifacts/research-proposal.md` consolida o gate de maturidade da fase de pesquisa, exigindo a declaração formal de hipótese, métricas e cronograma de trabalho.

## 3. Modos de Falha em Propostas de Pesquisa
1. **Proposta Tautológica:** Formular hipóteses óbvias que não admitem falseamento experimental (ex. "redes neurais podem aprender padrões").
2. **Omissão do Plano de Validação:** Descrever extensivamente a arquitetura do modelo mas não especificar como os dados serão divididos para prevenir vazamento de ensaios.

## O Que a Próxima Sala Assume
A próxima sala (`nt-thesis-methods`) — **Módulo Methods (padrão paper)** — redige a seção metodológica detalhada de um artigo científico em nível de publicação internacional.

## Artigos de Apoio e Leituras Recomendadas
- [MOABB documentation](https://neurotechx.github.io/moabb/) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [SPEC Neurotech](https://github.com/edevPedro/edge-mage/blob/main/docs/SPEC-neurotech-course.md) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
