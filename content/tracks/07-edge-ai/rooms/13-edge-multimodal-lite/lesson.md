# Multimodal lite no edge

Modelos multimodais de verdade (CLIP, MobileViT, BLIP) são caros para MCU; o caminho lite é **projetar embeddings compartilhados**: visão, áudio e texto mapeiam para um espaço comum onde similaridade = cosseno.

## Contrastive embeddings

O CLIP treina com contraste: pares relacionados ficam perto, não-relacionados longe. O resultado é (quase) um retriever de propósito geral. Na inferência edge:

```
similar = a·b / (|a||b|)     # cosseno em [−1, 1]
```

## Budget de memória

Para uma "memória" de embeddings (ex.: 128 possíveis sinais BCi/visuais):

```
bytes = dim · count · dtype_bytes      # 128 · 64 · 1 = 8 KB em int8
```

Batch de 64 × dim 128 em int8 deve caber na arena — e é isso que torna retrieval on-device plausível.

## Top-k na hora

Buscar o vizinho é `top_k` sobre as similaridades: ordinário em O(n·dim), barato quando n é pequeno (≤ centenas). Para corpora grandes, indexação é outro castelo — aqui o foco é status "lite": poc com cosseno sobre arena.

`cosine_sim` zera norma-zero (embedding nulo não rankeia), e `top_k_scores` devolve os índices dos k melhores — as duas peças de um retrieval lite.