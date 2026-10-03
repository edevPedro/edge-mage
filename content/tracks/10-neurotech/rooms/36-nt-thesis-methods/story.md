# História — A Seção de Métodos à Prova de Bala

Na bancada de redação de sua dissertação de mestrado, um pesquisador finaliza a seção de Métodos de seu trabalho sobre decodificação de imagética motora. Ele envia o manuscrito para revisão por pares simulada conduzida pela banca examinadora do laboratório.

Dois dias depois, a banca devolve o texto com anotações pontuais:
— Sua seção de Métodos está bem escrita, mas precisa cumprir o critério supremo da ciência contemporânea: **o teste do engenheiro cego** — pontua o presidente da banca. — Se um engenheiro no outro lado do planeta pegar apenas a sua seção de Métodos, sem ter acesso ao seu computador, ele deve ser capaz de reimplementar o pipeline exatamente como você fez e obter resultados idênticos até a terceira casa decimal.

O presidente da banca aponta as lacunas que precisavam ser preenchidas:
1. **Especificação de Filtros:** Em vez de "sinal filtrado entre 8 e 30 Hz", especificar: "Filtro passa-faixa causal Butterworth de 4ª ordem implementado em seções de segunda ordem (SOS), com atenuação de 40 dB em 60 Hz via filtro notch digital".
2. **Sementes e Versões:** Fixar a semente de números pseudoaleatórios (`seed=42`) e declarar as versões exatas das bibliotecas (`numpy 1.24`, `scipy 1.10`).
3. **Esquema de Particionamento:** Declarar expressamente: "Validação cruzada 5-fold agrupada por blocos de ensaios completos (GroupKFold), proibindo qualquer mistura temporal de janelas contíguas".

O pesquisador implementa uma rotina automática de validação de especificações (`validate_methods_spec`). Ele revisa a documentação no artefato `study-log/artifacts/neuro-thesis-methods.md`, detalhando cada equação, frequência de corte e critério de exclusão de artefatos.

Com a especificação validada pelo analisador de texto, a seção de Métodos atinge o padrão ouro de publicação internacional da IEEE e Nature Biomedical Engineering.
