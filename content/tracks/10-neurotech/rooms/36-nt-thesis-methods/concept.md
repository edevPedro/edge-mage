# Conceito — Redação de Métodos Reproduzíveis em Nível de Dissertação (IEEE/Nature Standard)

A seção de Métodos (Methodology) é a espinha dorsal de qualquer manuscrito científico ou relatório técnico em engenharia biomédica.

## 1. O Padrão de Reprodução Total
Para que a seção de Métodos seja considerada completa e reproduzível, ela deve especificar cumulativamente:
1. **Origem dos Dados e População:** Descrição dos participantes, dataset aberto utilizado (com link permanente/DOI) e aprovação ética de comitê institucional.
2. **Cadeia de Pré-Processamento:**
   - Frequência de amostragem ($f_s$).
   - Tipo de filtro (FIR ou IIR), ordem matemática, frequências de corte inferior e superior, e garantia de causalidade.
   - Algoritmo de remoção ou rejeição de artefatos com limiares numéricos exatos.
3. **Extração de Características e Modelagem:**
   - Formulação matemática completa (ex. formulação de covariâncias, CSP regularizado ou variedades Riemannianas).
   - Equações do classificador e função de perda.
4. **Protocolo de Validação Cruzada:**
   - Estratégia exata de particionamento (Leave-One-Run-Out ou Blocked K-Fold).
   - Garantia de isolamento estrito entre treino e teste.
5. **Reprodutibilidade Computacional:** Sementes pseudoaleatórias fixadas e versões de ambiente de software.

## 2. O Validador de Especificação de Métodos
A rotina `validate_methods_spec` atua como um linter de integridade científica, verificando se o checklist obrigatório contém todos os campos requeridos: `data`, `preprocessing`, `features_model`, `validation`, `seeds_versions` e `limits`.

## 3. Modos de Falha em Métodos Científicos
1. **Omissão da Direção do Filtro:** Não esclarecer se o filtro foi aplicado de forma causal (unidirecional) ou com `filtfilt` (bidirecional de fase zero).
2. **Falta de Semente Aleatória:** Omitir a semente de inicialização, fazendo com que cada execução produza acurácias diferentes e impedindo auditoria de terceiros.

## O Que a Próxima Sala Assume
A próxima sala (`nt-research-project`) — **Mini projeto de pesquisa (ritual)** — executa o projeto prático final de mestrado e confere a cobiçada Runa de Pesquisa (`rune-neuro-research`).

## Artigos de Apoio e Leituras Recomendadas
- [MNE-Python documentation](https://mne.tools/stable/index.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [sklearn User Guide](https://scikit-learn.org/stable/user_guide.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
