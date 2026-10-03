# Conceito — Stats para BCI (MSc)

## Unidade de análise

Trial / sessão / sujeito — não misture níveis ao reportar “acurácia média”.

## Chance level

2 classes equilibradas: acurácia esperada ≈ 0,5. Com desbalanceamento, calcule `p_e` da confusão esperada. **κ** (Schlögl) corrige acordo por acaso: `(p_o−p_e)/(1−p_e)`.

## Por que accuracy mente

- Classes desbalanceadas
- N pequeno (sorte)
- Leak inflando o número
- Múltiplas comparações (canais×bandas×clf) sem correção

## Incerteza

Reporte N, preferencialmente IC ou erro-padrão / distribuição de folds — não só o ponto.

## Combrisson & Jerbi

Stats em MEG/EEG: cuidado com testes e chance; DOI na sala. Use como freio ao overclaim.

## Ligação

`nt-hypothesis-power`, `nt-metrics-offline`, decode MVP.

## κ — interpretação rápida

| κ | Leitura pedagógica |
|---|--------------------|
| ≤0 | ≤ chance |
| 0.2–0.4 | fraco/moderado (contexto) |
| alto com N=10 | suspeito |

Não use cortes mágicos como verdade clínica — use como linguagem compartilhada + IC.

## Múltiplas comparações
20 canais × 6 bandas × 3 clf sem correção ≈ pesca. Pré-registre ou corrija / nested.

## Trabalhado: κ

p_o = 0.80, p_e = 0.50 → κ = (0.3)/(0.5) = 0.60.
Se p_e = 0.70 (desbalanceamento severo) e p_o=0.75 → κ = 0.05/0.30 ≈ 0.17 — accuracy “bonita” vira κ fraco.

## Bootstrap lite (ideia)
Resample trials, recalcule κ, reporte percentis — honesty melhor que ponto único. Não obrigatório na Sala, mas MSc-ready.

## Síntese em 4 bullets
- Ensina a reportar κ = (p_o − p_e)/(1 − p_e) e o p de permutação (1 + quantos nulos ≥ observado)/(1 + N), sem misturar trial, sessão e sujeito.
- A unidade é adimensional: com p_o = 0,65 e p_e = 0,5, κ = 0,30; observado 0,85 contra quatro nulos dá p = 2/5.
- Honesty: acurácia bonita com N pequeno, leak ou desbalanceamento não é efeito; κ ≤ 0 fica no acaso e não vira claim clínico.
- A sala seguinte no order é `nt-hypothesis-power`.

