# Conceito — Tokens: discretizar para gerar

Sinais contínuos (EEG, áudio) e texto discreto têm estruturas diferentes, mas
um modelo de sequência trata ambos como **tokens**: unidades de um vocabulário
finito ordenadas no tempo.

## 1. Do contínuo ao discreto
- Em DSP você amostra o tempo. Em modelos de linguagem, o *vocabulary* define
  as unidades discretas: chars → palavras → subwords.
- Cada token tem um id (`0..V−1`), e o `nn.Embedding` mapeia o id a um vetor
  aprendido. Fonte da latência: preencher o contexto em tokens.

## 2. Subword (WordPiece / BPE)
- Palavras raras são quebradas em pedaços (`unseen` → `un` + `seen`), contendo
  o vocabulário num tamanho razoável (~30k) e mantendo os tokens *frequentes*
  como unidades inteiras.
- Variações minúsculas de escrita ("run", "running") compartilham subwords —
  mais amostras por unidade aprendida.

## 3. Sequência: formato e não-formato
- Modelos esperam **batch retangular**: por isso *padding* (com id mascardo)
  e *truncation* ao tamanho do contexto.
- Analogia BCI: janelas de `n_samples` fixas com padding de trial — a mesma
  noção de "formato único para o tensor".

## O que a próxima sala assume
`nt-transformer-attn` usa tokens como entrada do mecanismo de atenção: cada
posição consulta as demais via Q/K/V.

## Leituras recomendadas
- [HF — tokenizers (subword)](https://huggingface.co/docs/tokenizers/en/)
- [WordPiece — Devlin et al.](https://arxiv.org/abs/1810.04805)
- [BPE — Sennrich et al.](https://arxiv.org/abs/1508.07909)