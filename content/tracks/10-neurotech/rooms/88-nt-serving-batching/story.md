# História — O Cacheiro que Entregava no Meio do Decode

O servidor de um chatbot educacional em hora de prova final era um desastre: o
throughput caía para metade quando 40 alunos pediam respostas longas ao mesmo
tempo. O logging mostrou o motivo: 39 requisições de 5 tokens estavam presas
esperando um colega gerar 400 tokens na mesma fila.

— Esse é o *static batching* — explicou a engenheira, desenhando dois retângulos
  no quadro. — Todos entram juntos e saem juntos. O batch inteiro só libera o
  cara mais lento. 80% das tokens passadas são do "rapaz do TCC".

Ela trocou para *continuous batching*. Agora, a cada token que o "TCC" terminava,
ele abria um slot: a resposta curta de 5 tokens entrava no meio do lote, gerava
tudo em 6 ticks, e saia — sem esperar ninguém. O throughput triplicou e as
respostas curtas vieram em segundos.

— TTFT justo, tokens/s alto — resumiu. — A fila não precisa ser justa com
  requisições de tamanhos diferentes; o scheduler sim.

Na parede do time pintaram: "batching não é encher a GPU. É encher a fila de
ouro: o slot livre não espera o mais lento."