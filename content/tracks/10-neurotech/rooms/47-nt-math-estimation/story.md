# História — O Viés Escondido na Pequena Amostragem

Em um teste preliminar de BCI embarcado em bancada, um desenvolvedor programa a rotina de inicialização que calcula a variância de ruído dos eletrodos durante um período de baseline de 4 epochs curtas. Ele utiliza a fórmula padrão de variância populacional aprendida em cursos introdutórios de computação: soma dos quadrados dos desvios dividida pelo número total de amostras $N$.

Os valores resultantes de variância são repassados ao estimador de SNR. No entanto, o filtro de Wiener calibrado com esses números rejeita agressivamente componentes do sinal verdadeiro, comportando-se como se o ruído fosse artificialmente baixo.

Ao auditar a biblioteca matemática, o engenheiro de sinais identifica a falha: para $N=4$, o divisor $N$ gera um valor que é sistematicamente igual a três quartos ($75\%$) da variância não enviesada. Um erro de viés de vinte e cinco por cento na estimativa de ruído estava descalibrando o filtro ótimo.

O desenvolvedor aprende na prática o impacto da correção de Bessel: em amostras biológicas limitadas, estimadores ingênuos de máxima verossimilhança carregam um viés matemático intrínseco de $(N-1)/N$. A rotina deve declarar e compensar esse viés explicitamente para garantir calibrações científicas reprodutíveis.
