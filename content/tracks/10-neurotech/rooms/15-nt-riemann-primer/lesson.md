# Lição

- SPD: simétrica definida positiva.
- Distância Riemanniana ≠ “só Frobenius”.
- Toy 2×2 **conceitual** na sala (MCQ/fill); papers reais nos resources.
- **Honestidade de ferramenta:** `spd_toy` no SPEC é conceito — **não há emulador shipped** (como `impedance_probe`). Use Yger/Congedo/Barachant + raciocínio SPD.
- Decode MVP (LDA) já passou — aqui é o salto geométrico opcional mas recomendado.

Para destravar o lab, abra [Barachant et al. — Multiclass brain–computer interface classification by Riemannian geometry (IEEE)](https://doi.org/10.1109/TBME.2011.2172210) e leia a distância em covariâncias SPD em Barachant (não a diferença euclidiana) para fechar riemann_diag_dist nas diagonais positivas.

## Lab estendido (obrigatório no Estuda)

1. Produza um artefato (tabela, diagrama ASCII ou pseudo-código ≤20 linhas) cobrindo o núcleo desta sala.
2. Calcule ou estime **um** número com unidade (Hz, µV, ms, dB, κ, Big-O, etc.).
3. Escreva a honesty note em 2 frases.
4. Liste pré-requisitos cumpridos (`requires_rooms`) e o que desbloqueia a seguir.
