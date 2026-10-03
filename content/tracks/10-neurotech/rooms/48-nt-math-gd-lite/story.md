# História — A Explosão Numérica da Taxa de Aprendizado

Durante o desenvolvimento de um firmware adaptativo de cancelamento de ruído bioelétrico para eletrodos de testa, um programador implementa uma rotina de gradiente descendente para ajustar em tempo real os coeficientes de filtragem linear. O objetivo é subtrair a contaminação de piscadas oculares sem deformar as oscilações cerebrais espontâneas.

Na primeira execução com dados reais digitalizados pelo conversor analógico-digital, o desenvolvedor escolhe arbitrariamente uma taxa de aprendizado $\eta = 2.0$, imaginando que uma taxa agressiva aceleraria a convergência do algoritmo antes do fechamento do buffer de áudio/streaming.

Os primeiros três frames parecem reduzir o erro residual. No quarto frame, a predição salta para dezenas de milhares de microvolts; no sexto frame, as variáveis de peso registram `inf` e disparam interrupções de hardware por falha de ponto flutuante no microprocessador.

O arquiteto de sistemas embarcados reúne o time para analisar o gráfico de estabilidade de Lyapunov: uma taxa de aprendizado desacoplada dos autovalores da matriz de dispersão de entrada transforma a descida de gradiente em um oscilador desestabilizado. O programador precisa calcular a descida de gradiente controlada, verificando analiticamente a contração da perda ao longo de épocas sucessivas com taxa de passo moderada.
