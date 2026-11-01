# História — O Redutor de Dieta do Modelo

A startup de copiloto embarcado tinha um problema físico: o modelo treinado em
fp32 pesava 7 GB, e o device de borda tinha 4 GB de RAM e um chip de NPU que
só acelerava int8.

O ML engineer testou fp16: 3,5 GB. Ainda não cabia. Ia devolver o device quando
a veterana segurou o mouse:
— Quantiza. Transforma os pesos em int8 — cada valor vira um inteiro e a escala
  guarda o intervalo. 7 GB vira 1,75 GB, e a NPU faz o matmul int8 2× mais
  rápido. Você só precisa checar que o erro que você introduz não destrói o
  κ do seu decoder.

Ele rodou PTQ com calibração de 512 batches: no papel, a validação caiu 0,8%.
O time reclamou:
— Caiu! Não está perfeito.
— Caiu 0,8% e você liberou 2× de ram e 2× de velocidade. Agora *mire o resto
  do orçamento* — o cache, as ativações — e meça de novo com os testes de
  latência de produção, não só com acurácia.

O gerente de produto brincou, apontando a etiqueta da versão do modelo no
release:
— fp32: 7 GB, 0,812 κ. int8: 1,75 GB, 0,804 κ. O 144% de memória economizada
  virou latência que o cliente sente. eu assino.

No lab, escreveram na parede: "otimização que não muda redmine, não otimiza."