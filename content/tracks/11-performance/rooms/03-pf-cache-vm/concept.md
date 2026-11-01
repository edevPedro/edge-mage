# Conceito — Hierarquia de memória

Latência sobe e capacidade sobe conforme se afasta dos registradores: L1 → L2 → LLC → DRAM → storage.

## Localidade

- **Temporal**: reusa o mesmo bloco logo.
- **Espacial**: acessa vizinhos no mesmo cache line (tipicamente 64 B).

Loops que saltam com stride grande destroem localidade espacial → *capacity/conflict misses*.

## VM e TLB

Tradução VA→PA usa page tables; o **TLB** cacheia traduções. Miss de TLB + walk caro aparece em working sets grandes ou páginas pequenas demais. Huge pages são trade-off (não bala de prata).

## Ligação com Performance

Tiling, prefetch e layout AoS/SoA existem para **caber** no nível certo da hierarquia. Sem esse modelo, NEON só move o gargalo.

