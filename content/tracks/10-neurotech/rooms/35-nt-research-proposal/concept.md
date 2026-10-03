# Conceito — Research proposal (gate MSc-prep)

Uma proposal neste círculo é um **contrato científico curto**, não um pitch. Deve caber numa página (ou 1–2) e responder: o que pergunta, com que dados, com que métrica, com que ética, em quanto tempo.

## Rubrica (SPEC gate)

| Bloco | Obrigatório | Falha típica |
|-------|-------------|--------------|
| **Pergunta** | 1 frase falsificável | “Explorar BCI” sem variável |
| **Hipótese** | Direção esperada (mesmo fraca) | Hipótese = método |
| **Dados** | synth / OA citado / humano+consent | HW sem ética |
| **Pipeline** | features + clf + split | “usar deep learning” sem CV |
| **Métrica** | κ + chance level (ou métrica do challenge) | só accuracy |
| **Ética** | Belmont lite + dual-use literacy | overclaim clínico |
| **Timeline** | semanas realistas | 2 dias para N=40 sujeitos |

## Template mental (IMRaD-prep)

```text
Intro (motivo + gap) → Methods plan → Expected Results → Risks/Ethics → Timeline
```

## Exemplos bons vs ruins

**Ruim:** “Vou ler pensamentos com EEG e 99%.”  
**Bom:** “Em MI 2-classes (C3/C4, mu/beta log-bandpower, LDA), κ offline com CV por trial em synth/OA será > chance; reporto IC e leak checks.”

## Ligação

`nt-paper-critique` → proposal → `nt-thesis-methods` → project → paper MSc. Casos Berlin/Comp IV servem de âncora de escopo.

## Exemplo preenchido (synth MI)

**Pergunta:** Em dados sintéticos com contraste mu/beta em C3/C4, um LDA em log-bandpower obtém κ significativamente acima de chance com CV trial-wise?

**Hipótese:** κ médio cross-validated > 0 (acima de p_e=0.5 em accuracy) com N≥80 trials balanceados.

**Dados:** `synth_eeg_stream` seed fixa; opcionalmente 1 dataset OA citado (Comp IV / Berlin literacy).

**Methods plan:** epoch → bank (8–12,16–24) → log-var → LDA → κ; nested só se tunar bandas.

**Ética:** sem sujeitos; dual-use literacy no texto; proibido overclaim clínico.

**Timeline:** 2 semanas pipeline + 1 semana escrita critique/proposal polish.

## Anti-padrões
- Proposal que é só lista de papers.
- Métrica “accuracy” sem chance.
- Timeline de tese completa numa sala.

