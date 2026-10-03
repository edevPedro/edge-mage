# Conceito — Banco de filtros para EEG / MI

## Ideia

Um **filter bank** aplica vários passa-banda (ex. mu 8–12 Hz, beta 16–24 Hz) e extrai energia/potência (ou covariância) por canal e por banda. É a ponte entre *ritmos nomeados* e *vetor de features*.

## Nyquist e honestidade elétrica

Dado `fs`, a frequência de Nyquist é `fs/2`. Bandas acima disso não são legais; perto de Nyquist, antialias (sala EE) importa. Escolher 40–80 Hz com `fs=100` sem filtro adequado é teatro.

## Separação de responsabilidades

| Etapa | Faz | Não faz |
|-------|-----|---------|
| Filter bank / pré-proc | isola bandas; reduz linha 50/60 | classificar rótulos |
| Features | bandpower / cov | decidir hiperparâmetros no teste |
| Classificador | LDA / etc. | “consertar” leak do pré-proc |

**Anti-leak:** estatísticas de filtro/normalização estimadas só no treino (ou com nested CV). Usar o teste para sintonizar cortes de banda invalida o número.

## Notch ≠ feature neural

Notch 50/60 Hz trata artefato de linha. Remover linha é higiene; reportar “descoberta neural em 60 Hz” é erro.

## Synth lab

`synth_eeg_stream` pode injetar contraste de energia por banda. Use para validar que o banco *isola* o que você pediu — **não** para afirmar ERD fisiológico.

## Runa

Esta sala dropa **`rune-neuro-acq`**. Cadeia eletrodo→terra→ADC completa pode conceder a mesma runa se o filter-bank ainda estiver aberto (ver SPEC).

Animação alvo: `filter_freq_response` — ganho na banda útil, atenuação fora.


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

