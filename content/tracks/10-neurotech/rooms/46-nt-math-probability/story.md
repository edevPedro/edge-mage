# História — A Curva Normal da Incerteza

Na bancada de calibração de um decodificador Bayesiano, uma pesquisadora analisa a distribuição estatística das potências de banda espectral de centenas de ensaios de EEG. Ela observa que, após a aplicação da transformação logarítmica, os dados se distribuem em uma curva suave em forma de sino perfeitamente centrada em torno de uma média $\mu$, com dispersão governada pelo desvio-padrão $\sigma$.

O desenvolvedor júnior que programa a função de verossimilhança pergunta:
— Por que não usamos uma distribuição uniforme simples entre o valor mínimo e máximo medidos para simplificar o cálculo do classificador?

A pesquisadora abre a função de densidade de probabilidade gaussiana no monitor:
— A distribuição normal não é uma conveniência arbitrária — explica ela. — Pelo Teorema Central do Limite, quando você mede o potencial elétrico no escalpo, você está observando a soma de milhões de pequenas correntes pós-sinápticas microscópicas independentes. A soma de muitas variáveis aleatórias independentes converge naturalmente para uma distribuição Gaussiana.

Ela demonstra como a probabilidade condicionada governa a decisão estatística:
— Para calcular a verossimilhança de que uma nova amostra $x$ pertença à classe de imagética da mão direita, precisamos avaliar a função densidade de probabilidade (PDF) normal:
$$p(x | \mu, \sigma) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)$$

O desenvolvedor implementa a função `gaussian_pdf`. O classificador bayesiano passa a atribuir probabilidades contínuas ponderadas em vez de limites rígidos, permitindo calibrar a incerteza do sistema e rejeitar comandos quando a probabilidade for ambígua.
