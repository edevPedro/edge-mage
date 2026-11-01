# História — O Mesmo Cérebro, Outros Sentidos

No último lab do módulo, o grupo apresentou projetos. Três destaques:
1. Uma aluna treinou um pequeno modelo CLIP-like e mostrou que a imagem do
   "cachorro" ficava perto do embedding textual "dog", mesmo usando um dataset
   minúsculo. Usou a mesma matemática de *contraste* da loss que o time de BCI
   usava para separar imagética motora.
2. Um aluno rodou difusão quantizada int8 em um notebook: a imagem saía, a um
   custo de 25 passos de denoising. Ele otimizou com 8 passos e cache de
   latente — qualidade sacrificada foi medida, não adivinhada.
3. O professor fechou com um exemplo BrC: "seu decoder de EEG pode ser o
   encoder de uma arquitetura multimodal — fala, texto e sinal no mesmo espaço."

Ninguém perguntou "vai funcionar?" no final. Todos perguntaram "quanto custa —
e qual é o p99?" Foi aí que a turma entendeu a lição final do roadmap: o
vocabulário da inferência — tokens, atenção, quantização, batching, métricas —
é o mesmo para todos os sentidos. O que muda é o formato do tensor.

E o estagiário da primeira sala, agora formado, resumiu com orgulho:
"Se você sabe o custo de uma premissa de unicórnio, você sabe o custo de um
chip em produção."