# História — O Deadline Invisível da Neuroprótese

Em uma sessão experimental em um centro de reabilitação robótica, um voluntário com lesão medular tenta controlar um exoesqueleto de membro superior acoplado a uma interface de BCI de imagética motora. O voluntário relata uma sensação profunda de desconexão e frustração: toda vez que ele imagina fechar a mão para segurar um objeto, o comando demora perceptivelmente para ser executado; quando o braço mecânico finalmente se move, o voluntário já relaxou a intenção, fazendo o robô abrir a mão novamente em oscilações instáveis.

O engenheiro sênior de sistemas de controle conecta um registrador de eventos de hardware para auditar a linha de tempo do ciclo fechado (closed-loop).

— No controle em malha fechada biológica, o sistema nervoso humano espera feedback sensorial em menos de 150 a 200 milissegundos após a intenção — explica o engenheiro. — Se o atraso total entre a emissão do biopotencial e a resposta física ultrapassar esse limite crítico (deadline), o usuário perde a sensação de agência e o sistema de controle entra em oscilação e instabilidade dinâmica.

Ele decompõe o orçamento de latência em suas três etapas canônicas:
1. **Janela de Sensoriamento ($t_{\text{sense}}$):** A rotina utilizava uma janela temporal deslizante de 2.0 segundos (2000 ms) para garantir espectro de frequência perfeito.
2. **Computação e Decodificação ($t_{\text{decide}}$):** O algoritmo de filtragem e inferência em Python levava 35 ms.
3. **Transmissão e Atuação ($t_{\text{act}}$):** O atuador eletromecânico e os comandos de rádio consumiam mais 40 ms.

— Somando as etapas, nossa latência total é $2000 + 35 + 40 = 2075\text{ ms}$! — exclamou o desenvolvedor júnior. — Estamos mais de dez vezes acima do deadline de 150 milissegundos!

O engenheiro sênior orienta a reformulação do orçamento: reduzir a janela deslizante de sensoriamento para 100 milissegundos (25 amostras a 250 Hz) com avanço contínuo a cada 40 milissegundos, otimizar o decodificador para executar em 3 milissegundos no microcontrolador, e calibrar o atuador para resposta em 30 milissegundos.

A nova latência total fecha em $100 + 3 + 30 = 133\text{ ms}$ — estritamente abaixo do deadline de 150 ms. Ao repetir o teste, o voluntário relata controle instantâneo e natural, segurando o objeto com estabilidade e precisão.
