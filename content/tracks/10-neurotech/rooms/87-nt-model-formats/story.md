# História — Um Modelo, Quatro Mundos

O mesmo EEGNet saiu da mesma sessão de treino e foi para três destinos: um
servidor de pesquisa, um aplicativo de celular e um MCU de 512 kB preso atrás
do eletrodo. O aluno ficou confuso: "é o mesmo modelo, por que formatos
diferentes?"

O mentor desenhou a tabela no quadro:
- Servidor: ONNX Runtime fp16 — GPU, batch de 64, kernel de atenção CUDA.
- Celular: LiteRT int8 com delegate de NPU — o mesmo forward, 4× menos bytes.
- MCU: TFLite-Micro quantizado, gráfico estático, sem Sistema Operacional —
  o forward cabe no cache do chip e roda sem alocação dinâmica.
- Notebook do pesquisador: GGUF fp32 pra ler os pesos e explorar.

— A diferença não é o modelo; é o contrato do device. Cada runtime pega os
  mesmos pesos e decide *como* executar — kernels, precisão, memória. Se você
  só quer 500 gravações de teste, o checkpoint basta; para produção, você
  assina um formato e valida A/B a acurácia e a latência.

O aluno ficou com a regra gravada na cabeça:
— Antes do runtime, o orçamento: quantos bytes? Antes do byte, a pergunta:
  onde roda? Antes de tudo: quanto custa a conversão em kappa?