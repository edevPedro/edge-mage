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

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-thesis-methods`) exige a redação formal e a validação computacional da seção de Métodos da dissertação, no padrão exigido por periódicos internacionais como IEEE Transactions e Journal of Neural Engineering.

## 5. Ponto de Destrave do Lab
Consulte o guia de elaboração de projetos de pós-graduação em engenharia de [Booth et al. (The Craft of Research, University of Chicago Press)](https://press.uchicago.edu/ucp/books/book/chicago/C/bo198544976.html).
