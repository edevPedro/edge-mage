# História — A Descida na Montanha do Erro

No laboratório de aprendizado de máquina adaptativo, um pesquisador programa um algoritmo de regressão logística para ajustar os pesos de um classificador de BCI online em tempo real. O modelo precisa atualizar continuamente o vetor de pesos $w$ a cada novo lote de ensaios para compensar a deriva de impedância dos eletrodos.

Na primeira execução, o pesquisador define uma taxa de aprendizado (learning rate) agressiva: $\eta = 10.0$.
Assim que os primeiros gradientes são calculados, os pesos explodem numericamente para valores de $10^{15}$, gerando overflow e predições `NaN`.

O professor de otimização numérica senta-se ao terminal e desenha a superfície de perda parabólica:
— A otimização por Gradiente Descendente é como descer uma montanha na escuridão guiando-se pela inclinação do chão sob os seus pés — explica o professor. — O vetor gradiente $\nabla L(w)$ aponta na direção da subida mais íngreme da função de erro. Para minimizar o erro, nós damos um passo no sentido oposto ao gradiente:
$$w_{\text{novo}} = w_{\text{atual}} - \eta \cdot \nabla L(w)$$

Ele demonstra a dinâmica da taxa de aprendizado:
— Se $\eta$ for excessivamente grande, você dá um passo tão longo que ultrapassa o fundo do vale e aterrissa mais alto do outro lado, divergindo em oscilações caóticas. Se $\eta$ for minúsculo demais, você demora milhares de iterações para convergir. O ajuste fino da taxa de aprendizado garante descida suave e convergência estável até o mínimo global da função de perda convexa.

O pesquisador implementa a função `gd_step` com taxa de aprendizado moderada e verificação de convergência. Os pesos convergem com precisão matemática para o mínimo global de erro, permitindo calibrações adaptativas contínuas e estáveis.
