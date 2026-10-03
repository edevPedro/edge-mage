# História — A diagonal que não é Frobenius

No canto do decode, duas covariâncias diagonais positivas esperam distância AIRM, não a diferença euclidiana dos autovalores. O guardião escreve `d1 = [1, e]` e `d2 = [1, 1]` e pede `riemann_diag_dist`.

A fórmula da Sala é a raiz da soma dos quadrados dos logaritmos naturais das razões: `sqrt(ln(1/1)^2 + ln(e/1)^2)`. O primeiro termo é zero. `ln(e) = 1`, o quadrado é 1, a raiz é 1. Frobenius em `(1−1, e−1)` dá outro número e não passa.

SPD aqui significa simétrica definida positiva — o toy é diagonal de propósito. Não há emulador `spd_toy` shipped; a conta é a prova. Barachant e o primer ficam como leitura, não como claim de que o MVP reproduz um paper Riemanniano. Se algum elemento for ≤ 0, o log deixa de ser real: a Sala não aceita “distância” de matriz que não é SPD.

Fase F8, nt-riemann-primer: riemann_diag_dist nesses dois vetores vale 1. Se a raiz der e−1, você usou diferença linear. O toy diagonal não autoriza dizer que o decode MVP já é Riemanniano.
