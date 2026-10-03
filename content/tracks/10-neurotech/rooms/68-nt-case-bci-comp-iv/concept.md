# Conceito — BCI Competition IV (literacia de challenge)

## Fonte âncora

Tangermann et al., *Review of the BCI Competition IV*  
DOI [10.1088/1741-2560/9/2/025009](https://doi.org/10.1088/1741-2560/9/2/025009)

Competições BCI (IIIa/IIIb/IV, etc.) padronizam **dados + tarefas + métricas** para comparar algoritmos com menos ambiguidade que demos isoladas.

## Por que importa no MSc-prep

1. Ensina a ler **task definitions** (o que prever, de que sinais, com que atraso).
2. Força métricas explícitas (não “deu certo no lab”).
3. Expõe diversidade de paradigmas (MI, P300, etc. — dependendo do dataset).
4. Âncora datasets abertos citáveis para o seu decode MVP.

## Mapa challenge → MVP do aluno

| Elemento do challenge | Pergunta que você responde | MVP neurotech |
|-----------------------|----------------------------|---------------|
| Dataset / sujeitos | De onde vêm os trials? | synth ou open data citado |
| Tarefa | Classes? Contínuo? | MI 2-classes toy |
| Features permitidas | Há restrição temporal? | bandpower / CSP primer |
| Métrica oficial | κ? acurácia? ITR? | κ + chance level + CV |
| Avaliação | Split oficial? | trial/subject split sem leak |
| Leaderboard | O que os top fizeram? | ideias — não copiar cegamente |

## Armadilhas

- Treinar no conjunto de avaliação do challenge.
- Reportar acurácia sem a métrica pedida.
- Misturar paradigmas (P300 speller ≠ MI ERD) no mesmo claim.
- Ignorar desbalanceamento de classes.

## Honesty

Walkthrough pedagógico ≠ reenvio oficial à competição. Cite Tangermann; declare limites do seu lab.


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

