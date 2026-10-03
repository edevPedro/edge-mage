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

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-cv-leakage`) estuda o esquema de particionamento aninhado (Nested CV) e auditoria estrita contra vazamento de ensaios.

## 5. Ponto de Destrave do Lab
Consulte o guia de desenho experimental e boas práticas em BCI de [Schlögl et al. (IEEE Trans Biomed Eng 2007)](https://doi.org/10.1109/TBME.2007.903711) e [Makeig et al. (Science 2002)](https://doi.org/10.1126/science.1066168).
