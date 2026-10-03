# História — O Mistério do Eletrodo Cego

Em uma sessão de calibração de um algoritmo de localização de fontes eletrofisiológicas, um cientista da computação posiciona um eletrodo exatamente sobre a coordenada somatotópica de representação da mão no córtex motor primário. Ele espera registrar a maior amplitude de potencial evocado somatossensorial naquele canal específico.

No entanto, para surpresa do programador, o eletrodo posicionado no zênite da área motora registra quase zero volts durante o estímulo, enquanto dois eletrodos periféricos situados a mais de quatro centímetros de distância registram deflexões de sinais fortes com polaridades rigorosamente invertidas.

O neurofisiologista da equipe desenha a anatomia dos giros e sulcos cerebrais no quadro: os corpos celulares dos neurônios piramidais que dispararam residem na parede interna do sulco central, formando um dipolo com orientação tangencial paralela à superfície craniana ($\theta \approx \pi/2$). Pela lei do dipolo eletrostático, a projeção sobre a normal do eletrodo superior é cancelada pelo cosseno do ângulo reto.

O desenvolvedor percebe que o escalpo não é uma tela de pixels: a física do dipolo impõe decaimento com o quadrado da distância ($1/r^2$) e cancelamento por orientação angular, exigindo modelos espaciais vetoriais para qualquer tentativa de interpretação coerente.
