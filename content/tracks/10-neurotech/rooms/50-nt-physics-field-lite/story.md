# História — O Silêncio das Fontes Profundas

Em uma discussão de desenho de projeto para controle de BCI, um desenvolvedor sugere capturar a atividade da amígdala e do hipocampo — estruturas subcorticais profundas situadas a mais de sete centímetros da superfície craniana — utilizando um eletrodo posicionado no topo da cabeça ($Cz$).

O neurofisiologista do laboratório pega um compasso e traça as esferas concêntricas da cabeça no quadro:
— No escalpo, nós enxergamos com clareza a atividade dos neurônios piramidais do córtex cerebral, situados a cerca de 1.5 a 2 centímetros dos eletrodos. Agora calcule a atenuação geométrica de uma fonte situada a 7 centímetros de profundidade.

O desenvolvedor lembra-se da lei do dipolo: o potencial decai com o quadrado da distância ($V \propto 1/r^2$).
Ele calcula a razão teórica de atenuação entre a fonte próxima ($r_{\text{near}} = 1.5\text{ cm}$) e a fonte profunda ($r_{\text{far}} = 7.0\text{ cm}$):
$$\text{Razão de Atenuação} = \left( \frac{r_{\text{far}}}{r_{\text{near}}} \right)^2 = \left( \frac{7.0}{1.5} \right)^2 \approx 21.78$$

— Apenas a distância geométrica pura reduz o sinal da amígdala por um fator de mais de vinte vezes em relação a uma fonte cortical superficial — demonstra o neurofisiologista. — E quando consideramos que a corrente da fonte profunda é borrada isotropicamente em todas as direções pela condução de volume do líquor e do crânio, a amplitude resultante no eletrodo de escalpo cai para menos de 0.1 microvolt — completamente soterrada pelo ruído térmico Johnson de 1 microvolt do próprio eletrodo.

O desenvolvedor compreende a limitação biofísica inegociável: o EEG não-invasivo de escalpo é uma ferramenta excelente para decodificar dinâmicas corticais superficiais (como os giros pré e pós-centrais do córtex motor), mas é fisicamente cego para dinâmicas subcorticais profundas sem eletrodos invasivos estereotácticos (sEEG).
