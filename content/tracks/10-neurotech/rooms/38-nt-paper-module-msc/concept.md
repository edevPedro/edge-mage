# Conceito — O Módulo de Artigo Científico em Nível de Mestrado (MSc Paper Module)

O módulo de artigo científico de mestrado (MSc Paper Module) é o artefato acadêmico que consolida a transição do desenvolvedor de software para um pesquisador e especialista autônomo em neuroengenharia.

## 1. Diferença entre Checkpoint e Paper Module MSc
Enquanto os checkpoints anteriores focam na replicação de um aspecto específico do pipeline:
- O **Paper Module MSc** exige a síntese completa: citação de artigo com DOI formal de acesso aberto, reprodução quantitativa de métricas, análise crítica de fraquezas e discussão aprofundada de limitações biofísicas e de engenharia.

## 2. A Função de Verificação de Reprodução
A rotina `verify_paper_reproduction(paper_meta, observed_metrics)` compara as métricas reportadas no artigo original contra as métricas observadas na replicação local:
- Calcula o desvio percentual relativo de acurácia e Kappa de Cohen:
  $$\text{erro\_relativo} = \frac{|\text{métrica\_observada} - \text{métrica\_reportada}|}{\text{métrica\_reportada}}$$
- Exige que o desvio permaneça dentro de uma margem aceitável de tolerância experimental (tipicamente $\le 15\%$) decorrente de diferenças de inicialização e sementes estocásticas.

## 3. Modos de Falha no Módulo de Mestrado
1. **Omissão da Discussão de Limitações:** Apresentar resultados como perfeitos sem apontar o impacto de fadiga do voluntário, artefatos residuais e restrições de generalização entre dias.
2. **Citação sem DOI Válido:** Fornecer links quebrados ou referências bibliográficas incompletas sem identificador persistente.

## O Que a Próxima Sala Assume
A próxima sala (`nt-mago-supremo`) — **Boss Mago Supremo (rota Neurotech)** — coroa a especialização com a auditoria rigorosa de todas as runas, artefatos e pipelines construídos ao longo do curso.

## Artigos de Apoio e Leituras Recomendadas
- [Yger et al. Riemannian review (HAL)](https://inria.hal.science/hal-01394253/document) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Barachant et al. DOI](https://doi.org/10.1109/TBME.2011.2172210) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Singh et al. DOI](https://doi.org/10.3390/s21062173) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
