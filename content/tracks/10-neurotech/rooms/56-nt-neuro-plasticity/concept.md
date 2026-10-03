# Conceito — Neuroplasticidade, Regra de Hebb e Não-Estacionariedade em BCI

## 1. A Hipótese de Hebb (1949)
Donald Hebb formulou o postulado biofísico da potenciação sináptica de longa duração (LTP):
> *"Quando um axônio da célula A excita repetidamente a célula B, participando de seu disparo, ocorre algum processo de crescimento ou alteração metabólica em uma ou ambas as células, aumentando a eficiência com que A dispara B."*

Informalmente: *"Neurons that fire together, wire together."*

A formulação matemática elementar para a atualização dos pesos sinápticos $w_{ij}$ entre uma ativação pré-sináptica $x_i$ e pós-sináptica $y_j$ com taxa de aprendizado $\eta$ é dada por:

$$\Delta w_{ij} = \eta \cdot x_i \cdot y_j$$
$$w_{ij}^{(t+1)} = w_{ij}^{(t)} + \Delta w_{ij}$$

## 2. A Quebra da Premissa i.i.d. em Neurotecnologia
Em ciência da computação tradicional, assume-se frequentemente que as amostras de treino e teste são variáveis aleatórias independentes e identicamente distribuídas (i.i.d.). Em interfaces cérebro-computador, essa suposição é categoricamente falsa:

1. **Variações Fisiológicas:** Atenção, fadiga, estresse e nível de alerta modulam continuamente a potência de base dos ritmos corticais.
2. **Deriva Eletroquímica:** A impedância na interface eletrodo-pele altera-se com a secagem gradual do gel condutor e microperspiração.
3. **Aprendizado do Voluntário:** O cérebro reorganiza a representação neural através de feedback proprioceptivo e visual, mudando os padrões de ativação espacial e espectral ao longo de dias e semanas.

## 3. Co-Adaptação e Protocolos de Calibração
O acoplamento humano-computador em BCI forma um sistema de aprendizado dinâmico de dois nós:
- **Nó 1 (Biológico):** O cérebro aprende estratégias cognitivas para acionar o decodificador com menor esforço e maior sinal-ruído.
- **Nó 2 (Sintético):** O decodificador computacional ajusta seus filtros espaciais e hiperplanos de separação para maximizar a separabilidade estatística.

Re-calibrações periódicas documentadas e métodos de adaptação de domínio (*domain adaptation*) são procedimentos padrão e metodologicamente honestos na literatura de neuroengenharia para mitigar a perda de calibração entre sessões.

## O Que a Próxima Sala Assume
A próxima sala (`nt-neuro-systems-bci`) — **Neuro — Sistemas e circuitos para BCI** — sintetiza a malha sensoriomotora e formaliza a métrica de dessincronização relacionada a eventos (ERD/ERS).

## Artigos de Apoio e Leituras Recomendadas
- [Wolpaw & Wolpaw BCI principles](https://doi.org/10.1016/j.clinph.2012.01.010) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
