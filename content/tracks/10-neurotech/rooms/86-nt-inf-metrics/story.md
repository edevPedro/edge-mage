# História — O Dashboard que Dizia Tudo Menos a Verdade

O novo dashboard de ML de uma fintech mostrava uma métrica única: "latência
média de resposta: 210 ms". A diretoria comemorou. O engenheiro sênior abriu o
mesmo dashboard em "p99" e congelou: 4.800 ms.

— A média está abaixo do SLA e o p99 está acima de *quatro segundos*. Metade
  das requisições chega em 30 ms; a outra metade fica presa numa fila do
  servidor de GPU — e depois explode. O cliente sente a cauda, não a média. E a
  pior parte: trocaram o batch da fila *sem medir* — achavam que estavam
  acelerando.

Ele puxou o roofline do kernel:
— Aqui: 38 FLOPs por byte. O modelo é *memory-bound* nessa máquina. Comprar
  GPU mais rápida quase não ajuda; quantizar o modelo corta os bytes e a cauda
  anda. Mas primeiro: *métricas de produção*, p95/p99, e depois qualquer
  mudança é uma hipótese com teste.

O dashboard ganhou três gráficos novos no mesmo dia: TTFT, ITL e p99 por
máquina. A diretoria nunca mais olhou para a média — e o time nunca mais
"otimizou" sem um N1 e um N2 (antes/depois) na tela.