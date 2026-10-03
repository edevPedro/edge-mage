# Conceito — BCI Assistivo, Métricas de Usabilidade e Acumuladores de Decisão

## 1. Princípios de Wolpaw para BCI Assistivo
Interfaces cérebro-computador assistivas têm como objetivo restaurar comunicação e controle para indivíduos com deficiências motoras severas (ex: ELA, lesões medulares completas, síndrome do encarceramento):
- O sistema não lê "pensamentos íntimos"; ele detecta intenções motoras ou atencionais voluntárias previamente acordadas.
- **Métricas Chave de Desempenho:**
  - **Taxa de Transferência de Informação (ITR):** Medida em bits/minuto ou caracteres/minuto, combinando acurácia, número de classes e tempo de seleção.
  - **Latência de Decisão:** O tempo necessário para acumular evidência neural suficiente para confirmar um comando.
  - **Fadiga e Carga Cognitiva:** Protocolos que exigem esforço atencional extenuante tornam-se inutilizáveis após poucos minutos de uso contínuo.

## 2. Limites Éticos e Proibição de Alegações Médicas
Projetos experimentais, protótipos acadêmicos e códigos deste curso são estritamente ferramentas educacionais e de pesquisa:
- **Proibição de Claims Clínicos:** Não é permitido rotular algoritmos ou hardwares prototipais como "dispositivos médicos certificados" sem os devidos ensaios clínicos aprovados por Comitês de Ética em Pesquisa (IRB/CEP) e homologação formal de agências sanitárias.
- O consentimento livre e esclarecido e a transparência metodológica são mandatórios em qualquer protocolo com participantes humanos.

## 3. O Acumulador de Evidência Temporal (Dwell Accumulator)
Para prevenir falsos disparos provocados por contrações musculares (EMG) ou ruído estocástico, utiliza-se a integração probabilística temporal:

$$S_t = \sum_{i=0}^t P_i$$

- A cada passo temporal $i$, o classificador fornece a probabilidade $P_i$ de que o usuário deseja confirmar o comando.
- O sistema acumula as probabilidades sequencialmente até que $S_t \ge \theta$ (*threshold*).
- O número de passos $t+1$ necessários para atingir o limiar define o tempo de permanência (*dwell time*). Se o sinal for ruído passageiro, o acumulador não atinge o limiar.

## O Que a Próxima Sala Assume
A próxima sala (`nt-app-neurofeedback`) — **Aplicação — Neurofeedback (literacy)** — projeta funções de recompensa linear retificada para autorregulação de ritmos cerebrais em malha fechada.

## Artigos de Apoio e Leituras Recomendadas
- [Wolpaw BCI principles](https://doi.org/10.1016/j.clinph.2012.01.010) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Singh et al. MI-BCI Sensors 2021](https://doi.org/10.3390/s21062173) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
