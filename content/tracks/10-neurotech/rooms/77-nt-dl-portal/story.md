# História — O Arquiteto que Perguntou "Pra Quê?"

No laboratório de neuroengenharia, um estagiário recebeu uma demanda curta: "deploy um decoder de imagética motora". Ele abriu o notebook, carregou um Transformer de 50 milhões de parâmetros e apertou *treinar*.

Três dias depois, a acurácia de teste era 49,5% — idêntica a um gerador de números aleatórios.

A coordenadora do laboratório aproximou-se com uma caneta e uma folha A4:
— Antes de você escolher o modelo, me responde três perguntas em linha reta:
1. Quantos trials você tem? — *"Cento e vinte."*
2. Quantas dimensões por trial? — *"48 mil, descompactando os 64 canais."*
3. Quantas vezes seu modelo divide o número de exemplos pelo de dimensões? — *"...zero vírgula quatro por cento, professora."*

Ela desenhou no papel a regra que abre este módulo:
— Aprender só importa quando há dados para aprender. Com N≪D, você não precisa de "mais deep": precisa de *inductive bias* que incorpore a física do sinal, e de uma função de custo honesta. Deep Learning é uma ferramenta poderosa — mas é preciso saber *quando* e *como* aplicar, e depois *como servir* esse modelo com latência, throughput e custo sob controle.

Ela abriu o roadmap.sh/inference-engineering no monitor:
— Este é o mapa: do forward de uma rede até servidores que batem orçamentos de latência e memória. A mesma disciplina que separa um *notebook toy* de um loop online real de BCI.

No fim do semestre, o estagiário apresentou o decoder final: EEGNet regularizada, validada cross-subject, e um relatório de latência mostrando onde cada milissegundo era gasto. Ninguém perguntou mais "pra quê?".