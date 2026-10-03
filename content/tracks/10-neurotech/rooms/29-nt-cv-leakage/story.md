# História — O Pecado Capital do Split Aleatório

Em uma competição acadêmica de decodificação neural, um participante submeteu um pipeline baseado em Support Vector Machines (SVM) que obteve 94% de acurácia em um dataset público de quatro classes de imagética motora. O participante utilizou a função padrão do Scikit-Learn `K-Fold(shuffle=True)` com 5 folds sobre o array de janelas processadas.

Ao rodar a validação cruzada do competidor em uma sessão independente do mesmo voluntário gravada no dia seguinte, a acurácia colapsou para 27%.

O comitê técnico do benchmark convocou o participante e demonstrou a causa da catástrofe analítica:
— Seu dataset continha 100 ensaios, mas você fatiou cada ensaio em 10 janelas temporais de 1 segundo com 80% de sobreposição — explicou o examinador. — Ao usar `shuffle=True`, você espalhou janelas que compartilham 800 milissegundos dos mesmos dados cerebrais entre o conjunto de treino e o conjunto de teste. O classificador decorou a microestrutura do ruído de fundo daquele segundo específico. Isso não é generalização; é o mais descarado vazamento de ensaio (trial leakage)!

O examinador explicou a regra de ouro da validação cruzada em neuroengenharia:
— A unidade indivisível de particionamento é o **ensaio completo** (ou o bloco de gravação / run), nunca a janela ou a amostra temporal! As amostras de um mesmo ensaio devem pertencer *integralmente* ao treino ou *integralmente* ao teste.

Ele introduziu o particionamento em blocos contíguos (`split_blocked_cv`) e a rotina de auditoria de vazamento (`audit_leakage`):
1. Verificar se a interseção entre os índices de treino e teste é estritamente vazia.
2. Garantir que nenhuma janela derivada de um trial de teste esteja presente nos folds de treino.

Com o particionamento em blocos independentes implementado, a acurácia real ajustada foi de 63% — livre de qualquer vazamento de dados e totalmente consistente com o desempenho em sessões futuras.
