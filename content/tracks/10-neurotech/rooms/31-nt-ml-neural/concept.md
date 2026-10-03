# Conceito — Machine Learning para Biopotenciais: A Barreira $N \ll D$ e EEGNet

O aprendizado de máquina sobre biopotenciais enfrenta restrições fundamentais de escassez de dados, não-estacionariedade e baixa relação sinal-ruído.

## 1. O Desafio de Dimensionalidade em Neurotecnologia ($N \ll D$)
- **Poucos Ensaios ($N$ pequeno):** Devido à fadiga do participante, sessões de calibração raramente excedem 100 a 200 ensaios por sujeito.
- **Muitas Dimensões ($D$ grande):** 64 canais amostrados a 250 Hz por 3 segundos geram $64 \times 750 = 48.000$ variáveis brutas por ensaio.
- **Risco de Overfitting Extremo:** Modelos de deep learning genéricos sem fortes restrições estruturais memorizam artefatos espúrios e falham na generalização entre sessões e entre sujeitos.

## 2. A Arquitetura EEGNet e Viés Indutivo Biofísico
Projetada por Lawhern et al. (2018), a **EEGNet** incorpora a biofísica de EEG diretamente na topologia de convoluções:
1. **Convolução Temporal 1D ($F_1$ filtros):** Aprende filtros digitais de frequência passa-faixa (equivalente ao filter-bank).
2. **Convolução Espacial Depthwise ($D$ por filtro temporal):** Combina linearmente os eletrodos espaciais em cada banda (equivalente a filtros espaciais CSP).
3. **Convolução Separável e Classificação:** Reduz dimensionalidade e projeta nas classes através de uma camada densa compacta com regularização de norma $L_2$ estrita e Dropout.

O total de parâmetros de uma EEGNet típica varia entre 1.500 e 3.000 pesos — quatro ordens de magnitude menor que redes de visão computacional.

## 3. Modos de Falha na Prática de Engenharia
1. **Complexidade Algorítmica Desproporcional:** Utilizar redes neurais profundas de milhões de parâmetros para resolver problemas binários simples de imagética motora onde CSP + Regularized LDA entrega acurácia superior com latência milissegunda em microcontroladores.
2. **Avaliação no Mesmo Bloco:** Validar modelos profundos sem teste rigoroso entre dias (inter-session) ou entre sujeitos (cross-subject).

## O Que a Próxima Sala Assume
A próxima sala (`nt-stream-buffer`) — **Stream sintético e ring buffer** — retorna à camada de sistemas conectando geradores contínuos de sinal ao buffer circular de streaming.

## Artigos de Apoio e Leituras Recomendadas
- [Lotte et al. classification review](https://doi.org/10.1088/1741-2560/4/2/R01) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Alzahab et al. Brain Sci. hDL-BCI (OA)](https://doi.org/10.3390/brainsci11010075) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [sklearn LinearDiscriminantAnalysis](https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
