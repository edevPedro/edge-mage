# História — O último valor, não a janela

Esta sala é a estrutura, não o stream de neuro. `Ring` com capacidade 3. O guardião empurra 1, depois 2, depois 3, depois 4. `latest()` devolve um escalar: o último valor escrito, que é 4.

Não é a lista `[2, 3, 4]`. Isso seria o `latest(n)` da sala de stream. Aqui a API é `push` e `latest` sem argumento de contagem. O 1 foi sobrescrito quando o quarto push chegou — política overwrite, a palavra do fill. Se `latest` devolver 1, você leu o slot mais antigo. Se devolver `[4]`, errou o tipo.

Capacidade fixa: o índice depois de `capacity − 1` volta a zero. Desenhe os três slots `[2, 3, 4]` e o cursor no 4. A conta é essa. Buffer infinito não existe no MCU didático, e não há amostra biológica nestes inteiros.

Fase F5, nt-cs-ringbuf-ds: latest() depois de push 1,2,3,4 numa capacidade 3 é o escalar 4. A política do fill é overwrite. Lista de três elementos é a API da outra sala de stream.
