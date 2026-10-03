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

## O Que a Próxima Sala Assume
A próxima sala (`nt-physics-electrostatics`) — **Física — Eletrostática e potencial** — faz a transição da matemática abstrata para a física dos campos eletrostáticos e a lei de Coulomb em meios condutores biológicos.

## Artigos de Apoio e Leituras Recomendadas
- [sklearn SGDClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
