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

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-closed-loop-control`) estuda BCI sob a ótica de sistemas de controle em malha fechada, atrasos de feedback sensorial e suavização exponencial (EMA).

## 5. Ponto de Destrave do Lab
Para o estudo da arquitetura canônica e código de redes compactas para EEG, consulte o artigo fundamental de [Lawhern et al. (J Neural Eng 2018, EEGNet)](https://doi.org/10.1088/1741-2552/aace8c) e o repositório oficial [EEGNet no GitHub](https://github.com/vlawhern/arl-eegmodels).
