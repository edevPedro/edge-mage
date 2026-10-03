# História — A Ilusão do Spike no Escalpo

Um engenheiro de software sênior recém-contratado por uma equipe de neuroengenharia acabara de debugar um modelo computacional de Hodgkin-Huxley em C++. Encantado com a precisão dos potenciais de ação simulados — picos esguios de 100 mV com duração de apenas um milissegundo —, ele propôs imediatamente à liderança técnica uma arquitetura revolucionária:

— "Se detectarmos os disparos individuais de cada neurônio motor no sinal de EEG, podemos decodificar a digitação do usuário tecla por tecla, sem precisar de janelas temporais de meio segundo."

O neurofisiologista do laboratório pousou a caneca de café na bancada e sorriu com paciência:

— "Seu modelo de Hodgkin-Huxley é matematicamente elegante para o axônio gigante de lula de 1952. Mas traga o eletrodo de superfície até o couro cabeludo. O que você enxerga no osciloscópio?"

O engenheiro olhou para o traçado: uma oscilação contínua, ruidosa, de meros trinta microvolts pico a pico. Nenhum spike afiado de um milissegundo era visível.

— "Onde foram parar os spikes?", perguntou o engenheiro.

— "Pense na física de condutores de volume e na escala temporal", explicou o pesquisador. "Um potencial de ação dura um milissegundo e viaja em axônios com orientações geométricas dispersas. Seus campos elétricos quadrupolares decaem com a terceira potência da distância e se cancelam quase perfeitamente no espaço extracelular. O que chega ao escalpo não é o disparo isolado de um neurônio, mas a soma coerente de centenas de milhares de correntes pós-sinápticas em neurônios piramidais alinhados paralelamente. Para entender a dinâmica celular sem cair na armadilha de achar que o EEG lê spikes individuais, você vai integrar o modelo mínimo de Euler de um neurônio Leaky Integrate-and-Fire. E vai entender onde a abstração celular termina e onde o sinal populacional de BCI começa."
