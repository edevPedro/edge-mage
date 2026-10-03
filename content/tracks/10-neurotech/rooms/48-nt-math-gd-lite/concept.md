# Conceito — Otimização Numérica: Gradiente Descendente e Atualização de Pesos

O algoritmo do Gradiente Descendente (Gradient Descent) é o motor computacional que ajusta parâmetros em modelos lineares generalizados, regressão logística e redes neurais profundas.

## 1. A Regra de Atualização do Gradiente Descendente
Dada uma função de perda diferenciável $L(w)$ parametrizada por um vetor de pesos $w \in \mathbb{R}^D$:
O gradiente $\nabla L(w)$ é o vetor das derivadas parciais:
$$\nabla L(w) = \left[ \frac{\partial L}{\partial w_0}, \frac{\partial L}{\partial w_1}, \dots, \frac{\partial L}{\partial w_{D-1}} \right]^T$$
O gradiente aponta na direção de maior crescimento da função. Para minimizar $L(w)$, o algoritmo atualiza os pesos iterativamente no sentido oposto:
$$w^{(k+1)} = w^{(k)} - \eta \cdot \nabla L(w^{(k)})$$
Onde $\eta > 0$ é a taxa de aprendizado (learning rate / passo de gradiente).

## 2. O Impacto da Taxa de Aprendizado ($\eta$)
- **$\eta$ Muito Alto:** Provoca divergência numérica (overshooting), onde o erro cresce exponencialmente a cada passo.
- **$\eta$ Muito Baixo:** Provoca convergência excessivamente lenta, tornando o treinamento inviável em hardware de tempo real.
- **$\eta$ Ótimo:** Garante descida monotônica do erro até a vizinhança do ponto ótimo $\nabla L(w^*) \approx 0$.

## 3. Modos de Falha na Prática de Engenharia
1. **Sinal Trocado (Gradiente Ascendente):** Somar o gradiente ($w + \eta \nabla L$) em vez de subtrair, maximizando o erro catastrófico.
2. **Gradientes Desaparecendo ou Explodindo:** Gradientes de magnitudes descalibradas devido a variáveis de entrada que não foram normalizadas para desvio-padrão unitário.

## 4. O que a Próxima Sala Assume
A próxima fase (`nt-physics-rc-tissue`) inicia o aprofundamento na física bioelétrica dos tecidos biológicos modelados como circuitos RC.

## 5. Ponto de Destrave do Lab
Consulte o guia clássico de otimização numérica em [Boyd & Vandenberghe (Convex Optimization, Cambridge University Press)](https://web.stanford.edu/~boyd/cvxbook/).
