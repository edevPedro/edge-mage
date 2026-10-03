# Conceito — Paradigma de imagética motora (MI)

## Definição

**Imagética motora (MI):** imaginar movimento (ex. mão esquerda/direita) sem necessariamente executá-lo. Em EEG de escalpo, marcadores clássicos envolvem ritmos **sensorimotores** (µ/β):

- **ERD↓** durante a imagética (dessincronização / queda de potência — convenção deste curso)
- possível **ERS↑** (rebound) após

Isto **não** é diagnóstico clínico nem leitura de conteúdo semântico do pensamento.

## Timing de trial (esqueleto pedagógico)

```text
ITI / baseline → cue → imagética (janela de interesse) → (rest / rebound) → ITI
```

| Segmento | Papel |
|----------|--------|
| Baseline | referência de potência |
| Cue | indica classe (L/R); cuidado com artefato visual |
| MI window | onde se estimam features |
| ITI | evita sobreposição; balanceamento |

Durações variam (papers: tipicamente poucos segundos de MI). O importante: **definir a janela antes** de minerar o teste.

## Lateralidade (aproximação 10–20)

- Imagética mão **direita** ↔ córtex motor esquerdo ≈ **C3**
- Imagética mão **esquerda** ↔ ≈ **C4**

Volume conduction e montagem misturam sinais — não espere separação perfeita canal-a-canal.

## Synth honesty

Contraste sintético de band-energy **não** é ERD de Pfurtscheller. Use synth para pipeline; cite papers para fisiologia.

## Fontes

- Pfurtscheller & Neuper DOI [10.1016/S0304-3940(97)00889-6](https://doi.org/10.1016/S0304-3940(97)00889-6)
- Pfurtscheller & Lopes da Silva DOI [10.1016/S1388-2457(99)00141-8](https://doi.org/10.1016/S1388-2457(99)00141-8)
- Padfield [PMC6471241](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/); Singh [PMC8003721](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/)


## Extensão MSc-prep (foundation → advanced)

### Modelo mental
1. **Definir** a grandeza / estrutura com unidades ou assinatura.
2. **Calcular** um exemplo numérico mínimo (mesmo que toy).
3. **Falhar com honestidade** — listar o que o modelo *não* captura (synth ≠ fisiologia; stub ≠ silício; κ sem chance level ≠ evidência).
4. **Ligar** à sala seguinte do mapa pedagógico (portal → pilares → espinha → online → research).

### Mini-lab escrito (15–25 min)
- Escreva um parágrafo Methods-style usando o vocabulário desta sala.
- Inclua uma métrica ou checklist observável (número, diagrama, ou critério pass/fail).
- Declare dados: synth / open dataset / HW eletivo.

### Rubrica rápida de autoavaliação
| Nível | Evidência |
|-------|-----------|
| Frágil | Só reconhece o nome do tópico |
| Operacional | Resolve o exercício da Sala e explica o porquê |
| Integrado | Conecta a CV/leak, SNR, latência ou ética conforme o pilar |

### Leitura ativa
Abra ≥1 resource do `room.yaml`, anote DOI/PMC, e escreva *uma* frase do paper/docs que esta sala operacionaliza.


## Profundidade full (espinha / EE avançada)

### Estudo dirigido (40–60 min)
1. Releia a tabela/equações do conceito e feche o arquivo; reescreva de memória.
2. Faça o lab numérico duas vezes com parâmetros diferentes (`fs`, banda, N).
3. Escreva um parágrafo ligando esta sala a **ética** (overclaim) e a **CV/leak** ou **SNR**, conforme couber.
4. Se houver paper DOI/PMC na sala, copie a frase Methods que você operacionaliza no MVP synth.

### Entregável de caderno
- Diagrama de 1 página (ASCII ok)
- 3 números com unidade
- 3 honesty bullets
- 1 pergunta para journal club

Isto eleva a sala do modo “trivia” para modo MSc-prep auditável.

