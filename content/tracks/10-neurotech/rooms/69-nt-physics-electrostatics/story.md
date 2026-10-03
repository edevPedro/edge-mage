# História — O Gradiente Invisível no Meio Condutor

Em uma bancada de modelagem computacional de fontes neurais, um estudante de física médica simula o campo elétrico gerado por duas populações corticais situadas a uma distância microscópica de 5 milímetros uma da outra. Ele mede que o potencial elétrico no primeiro ponto é de $+45\ \mu\text{V}$ e, no segundo ponto, é de $-15\ \mu\text{V}$.

O estudante tenta calcular a força que atua sobre os íons no espaço extracelular e questiona como relacionar o potencial escalar medido com o campo vetorial atuante.

O professor de eletromagnetismo abre a equação diferencial da eletrostática:
— Em física de biopotenciais, o potencial elétrico $V$ em Volts é um campo escalar de energia potencial por unidade de carga. Já o campo elétrico $\vec{E}$ é uma grandeza vetorial que descreve a força física exercida sobre cada Coulomb de carga iônica:
$$\vec{E} = -\nabla V$$

Ele demonstra a aproximação linear unidimensional para eletrodos separados por uma distância $\Delta x$:
$$E = -\frac{\Delta V}{\Delta x} = -\frac{V_2 - V_1}{d} = \frac{V_1 - V_2}{d}$$
— O sinal negativo é essencial: ele expressa que o campo elétrico sempre aponta no sentido do potencial decrescente, empurrando cátions positivos de áreas de alto potencial para áreas de baixo potencial — explica o professor.

Ele executa o cálculo com os dados da simulação:
$$E = \frac{45 \times 10^{-6} - (-15 \times 10^{-6})}{0.005} = \frac{60 \times 10^{-6}}{0.005} = 0.012\text{ V/m} = 12\text{ mV/m}$$

O estudante implementa a função `electric_field_from_potential`. Compreendendo que a corrente iônica macroscópica obedece à densidade de corrente $\vec{J} = \sigma \vec{E}$ através da condutividade tecidual $\sigma$, o modelo de fontes dipolares de EEG ganha consistência física completa.
