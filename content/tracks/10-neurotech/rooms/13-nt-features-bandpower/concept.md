# Conceito — Potência de Banda (Bandpower) e Espaço de Características

Em sinais eletrofisiológicos oscilatórios, a amplitude temporal instantânea possui média próxima de zero e fase instável. A potência média de banda (Bandpower) é a representação canônica que quantifica a energia rítmica para decodificação.

## 1. Formulação Matemática da Potência de Banda
Após o sinal ter sido processado por um filtro passa-faixa centrado na banda de interesse (por exemplo, ritmo $\mu$ de $8\text{--}12\text{ Hz}$), a potência média em uma janela de $N$ amostras é a variância do sinal com média zero:
$$P = \frac{1}{N} \sum_{n=0}^{N-1} x[n]^2$$

### A Transformação Logarítmica $\log(P)$
A distribuição das potências estimadas no tempo tende a ser assimétrica e de cauda longa (distribuição qui-quadrado). A aplicação do logaritmo:
$$f = \log_{10}(P) \quad \text{ou} \quad f = \ln(P)$$
produz duas vantagens matemáticas cruciais:
1. **Gaussianização dos Dados:** Aproxima a distribuição das características de uma normal multivariada, satisfazendo a premissa fundamental do Discriminante Linear de Fisher (LDA).
2. **Homogeneização de Variâncias:** Estabiliza a dispersão entre sujeitos com amplitudes basais muito diferentes.

## 2. Unidades e Ordens de Grandeza
- **Sinal de entrada ($x$):** Microvolts ($\mu\text{V}$).
- **Potência de banda ($P$):** Microvolts ao quadrado ($\mu\text{V}^2$).
- **Característica logarítmica ($f$):** Adimensional (escala logarítmica / decibéis relativos).

## 3. Modos de Falha na Prática de Engenharia
1. **Janela Temporal Curta Demais:** Calcular bandpower em janelas menores que 250 ms (para um ritmo de 10 Hz, isso representa menos de 2.5 ciclos), resultando em estimativas de variância instáveis e ruidosas.
2. **Logaritmo de Zero:** Se um canal saturar em zero constante, $\log(0) = -\infty$, quebrando a rotina de classificação numérica. Deve-se garantir um piso de estabilidade $\log(P + \epsilon)$ com $\epsilon = 10^{-10}$.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-decode-mvp`) conecta os vetores de potência de banda a um classificador linear LDA para calcular o hiperplano de separação e a métrica Cohen's Kappa.

## 5. Ponto de Destrave do Lab
Para fundamentar o uso de bandpower e log-variância em BCI, consulte o trabalho de [Müller-Gerking et al. (Electroencephalogr Clin Neurophysiol 1999)](https://doi.org/10.1016/S0013-4694(98)00115-9).
