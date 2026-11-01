# Desafio — Tokenização char-level

## 1. Objetivo do Desafio
Implementar o par encode/decode de um tokenizador didático (char-level), para
entender o contrato de id e o papel do vocabulário antes de qualquer modelo.

## 2. Especificação Técnica e Formulação
- `encode(text, vocab)`: para cada caractere `ch` em `text`, faça
  `vocab[ch]` → lista de ids. Char desconhecido → levanta `KeyError`.
- `decode(ids, vocab)`: inverte o mapeamento → `id→vocab_inv[id]` e concatena.

## 3. Critérios de Validação e Armadilhas
- O vocabulário mapeia `str → int`; a inversão usa o *indice* como chave.
- `decode` deve aceitar qualquer lista de ids; ids fora do vocabulário →
  `KeyError`.
- Cheque redondeza: `decode(encode(s, vocab), vocab) == s`.