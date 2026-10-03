# Lição — Escrever a proposal

## Objetivos

Entregar uma mini-proposal que passa a rubrica SPEC (pergunta, hipótese, dados, métrica, ética, timeline).

## Passos

1. Escolha **uma** pergunta binária MI (ou SSVEP eletivo) — não três.
2. Fixe dados: preferir synth + 1 dataset OA citado; humano só com consentimento.
3. Escreva pipeline em 5 caixas: epoch → filter → feature → clf → κ/CV.
4. Declare anti-leak (split por trial/sujeito).
5. Ethics: 5 bullets Belmont + “não overclaim”.
6. Timeline: 4–8 semanas realistas para o *slice* (não a tese inteira).

## Lab (entregável)

Documento `proposal.md` com secções da rubrica. Inclua:
- fórmula de κ e `p_e` para seu desenho
- N trials planejado (ordem de grandeza) e por quê
- 1 risco dual-use *literacy* (sem receita)

## Checklist Sala

- [ ] Pergunta falsificável
- [ ] Métrica ≠ só accuracy
- [ ] Ética explícita
- [ ] Timeline não fantasia

## Caderno (domínio)

Escreva 1 página: (1) diagrama desta sala, (2) 3 números com unidade, (3) honesty note, (4) ligação à sala anterior e seguinte do PEDAGOGICAL path. Isto conta como Estuda completo antes da Sala.

Para destravar o lab, abra [MOABB documentation](https://neurotechx.github.io/moabb/) e leia como o MOABB declara dataset e avaliação, para a proposta nomear dados abertos e κ como métrica primária.
