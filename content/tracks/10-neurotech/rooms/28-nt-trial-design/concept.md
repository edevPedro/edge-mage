# Conceito — Desenho Experimental de Ensaios (Trial Design) e Mitigação de Vieses

O desenho experimental rigoroso é a barreira contra vieses de expectativa do participante, fadiga cognitiva e deriva eletroquímica de hardware.

## 1. Estrutura Temporal do Ensaio Canônico
Um ensaio (trial) bem projetado segue fases temporizadas:
- **Baseline Pré-Ensaio ($1.0\text{--}2.0\text{ s}$):** Fixação visual e repouso basal.
- **Aviso e Estímulo ($0.25\text{--}0.5\text{ s}$):** Marcador temporal (trigger/cue).
- **Período de Execução Mental ($3.0\text{--}4.0\text{ s}$):** Janela de análise de ERD/ERS.
- **Intervalo Inter-Ensaios (ITI) com Jitter ($1.5\text{--}2.5\text{ s}$):** Intervalo com duração estocástica para evitar acomodação temporal e potenciais lentos de antecipação (Contingent Negative Variation - CNV).

## 2. Pseudoaleatorização e Sequência Máxima (Max Streak)
Para evitar que o participante tente adivinhar a próxima classe ou desenvolva estratégias de aposta:
- O número de ensaios de cada classe deve ser rigorosamente igual em cada bloco experimental.
- A sequência contígua máxima da mesma classe (`max_streak`) deve ser limitada a 2 ou 3 repetições consecutivas.

## 3. Modos de Falha no Desenho Experimental
1. **Apresentação em Blocos Monótonos:** Executar toda a Classe 1 pela manhã e toda a Classe 2 à tarde, confundindo variações circadianas e deriva de gel condutor com sinal biológico.
2. **ITI Fixo e Previsível:** Usar intervalos exatamente iguais a 2.000 segundos, fazendo com que ondas de expectativa do córtex frontal contaminem a linha de base pré-estímulo.

## O Que a Próxima Sala Assume
A próxima sala (`nt-stats-bci`) — **Stats para BCI (N, κ, chance)** — aplica testes estatísticos de significância para verificar se a acurácia de decodificação supera a probabilidade de acerto ao acaso.

## Artigos de Apoio e Leituras Recomendadas
- [Pfurtscheller & Neuper 1997 — MI activates S1/M1](https://doi.org/10.1016/S0304-3940(97)00889-6) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Blankertz et al. Berlin BCI (OA)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5116473/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Lab Streaming Layer](https://labstreaminglayer.readthedocs.io/) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
