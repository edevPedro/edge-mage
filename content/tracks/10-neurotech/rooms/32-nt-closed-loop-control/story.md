# História — O Feedback que Instabilizou o Robô

Em uma demonstração de teleoperação em malha fechada em um laboratório de robótica assistiva, um voluntário utiliza um decodificador de BCI para guiar um cursor na tela em direção a um alvo. O decodificador emite predições brutas a cada 50 milissegundos. Toda vez que uma predição instantânea flutua ligeiramente devido a um piscar de olhos ou desvio estocástico de sinal, o cursor dá um solavanco violento para o lado oposto.

O voluntário tenta corrigir o erro olhando assustado para o movimento espúrio do cursor. A reação visual gera uma onda P300 e aumento de desincronização motora caótica; o decodificador interpreta essa reação como novo comando de movimento, e o cursor entra em um ciclo incontrolável de oscilação divergente (hunting effect).

O engenheiro de controle e automação aproximou-se da bancada e abriu o diagrama de blocos do sistema em malha fechada:
— Um BCI em tempo real não é um sistema estático de classificação de fotos; é uma malha fechada de controle onde o cérebro humano é o controlador mestre, a interface de processamento de sinal é a planta, e os olhos do usuário recebem o feedback sensorial com um atraso biológico inegociável de cerca de 150 a 200 milissegundos.

Ele apontou a falha no código de acoplamento:
— Se você alimentar a saída do classificador diretamente no atuador sem filtragem temporal, você injeta ruído de alta frequência em um sistema com atraso de transporte. Qualquer atraso no feedback visual somado ao ganho alto da interface provoca oscilação sustentada e instabilidade dinâmica.

Ele implementou a suavização exponencial adaptativa (Exponential Moving Average - EMA):
$$y_{\text{smooth}}[t] = \alpha \cdot y_{\text{raw}}[t] + (1 - \alpha) \cdot y_{\text{smooth}}[t-1]$$
Com $\alpha = 0.25$, os comandos espúrios de alta frequência foram amortecidos, preservando a intenção contínua e suave do voluntário. O cursor estabilizou-se imediatamente, permitindo trajetórias elegantes e precisas até o alvo.
