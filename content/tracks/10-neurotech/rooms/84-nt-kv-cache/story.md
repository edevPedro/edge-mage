# História — O Megabyte que Comeu o Servidor

O time de infra recebeu um alerta: VRAM 100% às 14h37, tão rápido quanto o
horário de pico das respostas do assistente de e-mail.

O engenheiro rodou `nvidia-smi` e não encontrou bola de cristal — encontrou o
**KV cache**. Ninguém reprocessava o contexto; todo mundo olhava para a atenção
do token novo contra o passado. Só que cada requisição guardava chaves e valores
de *toda* a conversa: 2 mil tokens × 32 camadas × 32 cabeças × 128 dimensões ×
2 (chave e valor) × 2 bytes = 2,14 GB por usuário ocupado. Com 3 janelas de
chat no pico, a conta virou 6,4 GB sem modelo nenhum.

— E isso cresce a cada token — disse o engenheiro — e *sofre de fragmentação*:
cada sessão aloca seu bloco contíguo, e os buracos entre eles são inúteis.

A solução não foi comprar VRAM. Foi **PagedAttention**: o cache passou a ser
paginado em blocos pequenos, alocados quando precisavam, compartilhando até
prefixos comuns entre usuários (todos que mandaram "bom dia!" na mesma onça
reutilizavam o mesmo cache). A fragmentação sumiu e o pico de 14h37 voltou a
ser 100 requisições confortáveis.

Na retrospectiva, alguém lembrou: "Pesos são livres. Cache é aluguel."