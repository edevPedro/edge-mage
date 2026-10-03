# Conceito — Ring buffer (DS)
Buffer circular: head/tail mod N. `push` sobrescreve se cheio (política: drop oldest vs block). `latest(n)` para janela online.
## Falhas
underrun (consumer pede o que não há), overrun (perde amostras), data race sem sync.
## Ligação
`nt-stream-buffer`, `nt-cs-realtime-testing`.

## Por que está no caminho MSc-prep
Este tópico (Ring buffer) ancora o pilar: sem ele, salas à frente viram procedimentos sem modelo mental.

## Erros comuns
1. Memorizar buzzword sem unidade / equação / contraexemplo.
2. Misturar escala (single-trial vs sujeito vs população).
3. Overclaim a partir de synth ou N pequeno.

## Exercícios mentais
- Defina estrutura circular para stream EEG em uma frase.
- Dê um contraexemplo onde ignorar isto quebra κ ou SNR.
- Cite uma sala vizinha que depende desta.

## Leitura
Use os resources do `room.yaml` desta sala; priorize DOI/PMC já listados.


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

