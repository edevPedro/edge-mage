# História — A Camada que Não Sabia Sair do Zero

Um grupo de iniciação científica reconstruiu do zero um decodificador de
imagética motora "só com NumPy". No primeiro teste de sanidade, o forward de uma
camada de 256 neurônios manteve as saídas idênticas entre dois inputs diferentes.

A veterana do grupo olhou o código:
— Onde está a função de ativação?
— Eu usei *linear puro*. Uma camada já dá *qualquer* função, né?
— Teoricamente quase, mas na prática: sem ReLU, suas "camadas" colapsam
  numa única multiplicação de matrizes. Dois inputs diferentes ficam iguais
  se a matriz for degenerada — que é exatamente o que acontece com pesos
  simétricos no início do treino.

Ela corrigiu o forward com `max(0, z)` no meio e pediu outra coisa:
— Agora me diz quantos parâmetros tem a rede: 8 features → 256 → 4 classes.
— 8×256 + 256 + 256×4 + 4 = 3084.
— Certo. E me diz *por que* 3 neurônios escondidos não dariam resultado melhor
  mesmo com menos parâmetros.
— Vou chutar que não é tão simples...

— Não é, mas é o ponto: profundidade compõe features, mas cada neurônio a mais
  custa parâmetros. No teu dataset de 120 trials, a rede que vence não é a mais
  profunda — é a que cabe no dado. Primeiro mais *dados honestos* e
  regularização; depois profundidade.

A cena virou o mantra do laboratório: "a camada mais cara é a que não aprende —
e a segunda mais cara é a que memoriza."