# História — A Miragem do Periodograma Bruto

Na sala de processamento de sinais de um centro de neurotecnologia, um desenvolvedor analisa a resposta em frequência de um canal de eletroencefalografia gravado durante uma tarefa de relaxamento com olhos fechados. Ele utiliza a transformada rápida de Fourier direta sobre o epoch inteiro de quatro segundos (1000 amostras a 250 Hz) para calcular o periodograma bruto: $|\text{FFT}(x)|^2 / N$.

Na tela, o gráfico espectral parece uma floresta de agulhas irregulares:
— O pico de 10 Hz está aqui — diz o desenvolvedor apontando para a tela —, mas ele está cercado por dezenas de espículas caóticas de amplitudes quase iguais em 9.5 Hz, 10.2 Hz e 10.8 Hz. A variância do espectro está tão alta que o algoritmo de rastreamento de pico oscila a cada ensaio.

O pesquisador de DSP do laboratório aproxima-se e recorda o teorema fundamental da teoria espectral:
— O periodograma direto sobre uma série temporal estocástica finita não é um estimador consistente — ensina o pesquisador. — À medida que aumentamos o número de pontos $N$, a resolução em frequência melhora ($\Delta f = 1/T$), mas a variância da estimativa em cada frequência *não diminui*. Você tem cada vez mais pontos ruidosos, mas a mesma incerteza estatística em cada um deles.

Ele introduz o clássico método de Welch (1967):
1. Particionar o sinal contínuo em sub-janelas temporais sobrepostas (tipicamente com 50% de overlap).
2. Multiplicar cada segmento por uma janela suave (como a janela de Hanning) para atenuar as bordas e suprimir o vazamento espectral (spectral leakage).
3. Calcular o periodograma de cada segmento isoladamente.
4. Tirar a média das potências através de todos os segmentos.

O desenvolvedor implementa a rotina de Welch. A floresta de agulhas ruidosas colapsa instantaneamente em uma curva suave e elegante: o pico de ritmo alfa em $10.1\text{ Hz}$ destaca-se com estabilidade estocástica perfeita e relação sinal-ruído cristalina.
