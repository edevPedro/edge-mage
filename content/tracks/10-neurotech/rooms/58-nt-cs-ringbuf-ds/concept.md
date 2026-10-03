# Conceito — Estrutura de Dados Ring Buffer (Buffer Circular)

## 1. Princípio de Funcionamento
Um buffer circular (*ring buffer*) é uma estrutura de dados de tamanho fixo alocada contiguamente na memória que opera conceitualmente como se as extremidades estivessem conectadas:

- **Capacidade ($N$):** Quantidade máxima de elementos que a estrutura armazena.
- **Ponteiro de Escrita (`write_ptr` ou `head`):** Índice do próximo slot onde uma nova amostra será inserida.
- **Avanço Modular:** Ao atingir o final do array, o índice retorna a zero através da operação de módulo:
  $$\text{head}_{next} = (\text{head} + 1) \pmod N$$

## 2. Política de Sobrescrita (*Overwrite*) vs. Bloqueio
Em sistemas de telecomunicações comuns, filas de mensagens frequentemente bloqueiam o produtor quando estão cheias. Em interfaces cérebro-computador e streaming eletrofisiológico:
- O produtor (conversor analógico-digital ou DMA do microcontrolador) nunca pode ser bloqueado; a biologia não espera o processador.
- Se o consumidor de processamento atrasar, o buffer circular adota a política de sobrescrita (*overwrite*): a amostra mais antiga é descartada em favor da amostra recém-chegada.
- Isso garante que a janela de análise temporal reflita sempre o estado neural mais recente do usuário.

## 3. Acesso ao Elemento Mais Recente (`latest`)
Em tarefas de decodificação preditiva em malha fechada, os filtros espaciais frequentemente precisam inspecionar o último valor registrado no stream sem precisar percorrer toda a fila. O método `latest()` deve retornar em tempo constante $\mathcal{O}(1)$ o elemento que acabou de ser gravado pelo último comando `push`.

## O Que a Próxima Sala Assume
A próxima sala (`nt-cs-numerics`) — **CS — Estabilidade numérica** — trata do cancelamento catastrófico em ponto flutuante e da regularização diagonal (shrinkage) de matrizes de covariância mal-condicionadas.

## Artigos de Apoio e Leituras Recomendadas
- [Wikipedia — Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Python collections.deque](https://docs.python.org/3/library/collections.html#collections.deque) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
