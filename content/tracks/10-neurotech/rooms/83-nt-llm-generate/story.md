# História — O Oráculo de 30 Tokens por Segundo

O serviço de uma startup de "copiloto clínico" travava. Cada resposta de 200
tokens levava 40 segundos. O CEO pedia a promessa antiga do vendor: "prefill
paralelo, moderna arquitetura". O engenheiro pleno abriu o trace e apontou a
distribuição:

— O primeiro token saiu em 300 ms — esse é o prefill: todo o contexto em
  paralelo, TTFT lindo. Os outros 42 segundos são o decode: **token a token**,
  150 ms por token, 6,6 tokens/s. A paralelização não ajuda porque cada passo
  seguinte depende do anterior. É 199 caminhadas, não um salto.

Ele abriu o código do servidor:
— E o pior: cada passo reprocessava o contexto inteiro em vez de usar o cache.
  Corrigi para reutilizar o KV do prefill — o mesmo token saiu a 28 tokens/s,
  latência por token em 35 ms.

No quadro, escreveu a lição que passou a nortear o time:

```
prefill = paralelo, computa o contexto (TTFT ↑ se o prompt for longo)
decode  = sequencial, usa o cache KV   (ITL & tokens/s dominam)
melhore o decode e o cache ANTES de comprar mais GPU
```

O CEO nunca mais perguntou pela arquitetura. Só perguntou a latência por token.