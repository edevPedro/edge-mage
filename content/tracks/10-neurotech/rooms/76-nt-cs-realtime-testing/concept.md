# Conceito — CS avançado para streaming BCI

## Além do harness unitário

| Teste | Alvo |
|-------|------|
| Unit | funções de feature/κ |
| Property | ringbuf wrap, latest(n) |
| Realtime | deadline miss rate, underrun count |
| Integration | `online_stub` com stream synth |

## Sinais de falha

- Underrun / overrun
- Jitter > orçamento
- Relógio lógico ≠ wall clock
- Logs sem timestamp monotonic

## Ligação

`nt-cs-ringbuf-ds`, `nt-stream-buffer`, `nt-latency-budget`, `nt-online-stub`.


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


## Caderno do aluno (bloco denso)

### Glossário mínimo (preencha com suas palavras)
- Termo A → definição + unidade
- Termo B → definição + unidade
- Termo C → anti-exemplo (o que *não* é)

### Derivação / algoritmo em 5 linhas
Descreva o núcleo operacional desta sala como sequência:
entrada → transformação → saída mensurável → critério de qualidade → falha típica.

### Exemplo numérico guiado
Escolha números redondos compatíveis com EEG/BCI educacional:
- fs ∈ {128, 250, 512} Hz
- bandas mu/beta ou SNR em dB
- latência em ms ou κ ∈ [-1, 1]
Calcule à mão ou com pseudo-código e registre o resultado.

### Ligação multi-pilar
Escreva uma seta:
Math/Physics/EE/Neuro/CS/FW → **esta sala** → Decode/Online/Research.
Explicite *uma* dependência de cada lado.

### Ética e honesty (sempre)
Se houver sujeito humano, consentimento vem antes. Se houver synth, declare que não é ERD fisiológico.
Se houver MCU stub, declare que não é QEMU/ciclo-acurado. Se houver κ, declare chance level e CV.

### Checklist de saída (Estuda completo)
- [ ] Glossário preenchido
- [ ] Exemplo numérico feito
- [ ] Honesty note escrita
- [ ] Resource DOI/PMC aberto pelo menos uma vez
- [ ] Pronto para tasks da Sala sem “chute de MCQ”

