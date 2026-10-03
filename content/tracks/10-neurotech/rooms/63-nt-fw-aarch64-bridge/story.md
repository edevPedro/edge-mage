# História — A Ponte Entre o Python e o Silício

No laboratório de computação de borda, um engenheiro de aprendizado de máquina terminara de treinar um modelo de filtragem espacial para um sistema de BCI móvel em um laptop com Intel Core i9. Para projetar os 64 canais de EEG em componentes independentes, o script executava uma multiplicação matricial contínua:

$$Y = W \cdot X$$

— "O código em Python está pronto para embarcar no gateway da cadeira de rodas", disse ele, entregando um pendrive com o script `.py` para a equipe de sistemas.

O engenheiro de computação embarcada plugou o código em uma placa industrial baseada no processador ARM Cortex-A72 de 64 bits (arquitetura AArch64):

— "Seu script no host leva 18 milissegundos para rodar uma projeção linear porque o interpretador Python serializa cada multiplicação escalar uma a uma na CPU. Nosso gateway precisa processar o sinal a cada 2 milissegundos para manter o controle postural estável."

Ele abriu a documentação de instruções vetoriais Neon de 64 bits da ARM:

— "Neste curso e nos ambientes de prototipagem, nós frequentemente usamos *stubs* em Python no host para validar a lógica matemática e os testes conceituais. Mas em produção no Edge real, nós usamos extensões SIMD (Single Instruction, Multiple Data). Os registradores Neon de 128 bits processam quatro números float32 simultaneamente com uma única instrução de máquina `FMLA` (Fused Multiply-Accumulate)."

O engenheiro sentou ao teclado com o novato:

— "Para entender como a álgebra linear de neuroengenharia roda no silício sem depender de bibliotecas pesadas de terceiros, você vai implementar a operação fundamental que o hardware faz: o produto escalar vetorizado de 4 elementos (SIMD-4). Compreender a diferença entre o modelo mental didático do host e as instruções reais de silício é o que distingue um cientista de dados de bancada de um engenheiro de neurotecnologia de produção."
