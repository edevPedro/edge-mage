# Conceito — Caso Berlin BCI (walkthrough pedagógico)

## Fonte âncora

Blankertz et al., *The Berlin Brain–Computer Interface: Progress Beyond Communication and Control* — Frontiers in Neuroscience  
[PMC5116473](https://pmc.ncbi.nlm.nih.gov/articles/PMC5116473/) · DOI [10.3389/fnins.2016.00530](https://doi.org/10.3389/fnins.2016.00530)

## O que o caso ensina (neste círculo)

1. **Histórico / motivação** de um lab maduro de MI / SMR.
2. **Pipeline típico** (estágicos) que você deve reconhecer no seu MVP.
3. **Honestidade de escopo**: feedback online, usuários reais, desafios de transferência — não um notebook de 20 linhas.
4. **Como ler** Methods/figuras: estágio a estágio, sem fingir reprodução completa.

## Estágios → seu pipeline synth (mapa)

| Estágio no paper (genérico MI lab) | Analogia no MVP do aluno |
|------------------------------------|---------------------------|
| Captação EEG / montagem | `synth` ou dataset aberto; EE real = eletivo ético |
| Pré-processamento / filtros | filter-bank mu/beta; anti-leak |
| Features (CSP / bandpower / …) | bandpower toy → depois CSP primer |
| Classificação | LDA toy / sklearn |
| Avaliação | κ, chance level, CV por trial/sujeito |
| Online / feedback | `online_stub` + latency budget |
| Limites / usuários | paper critique + ethics |

## O que NÃO é este exercício

- Reprodução bit-a-bit de resultados Berlin.
- Afirmar equivalência synth ↔ sujeitos Berlin.
- Usar figuras do paper sem atribuição / fora de fair use pedagógico.
- Overclaim clínico.

## Como caminhar o PMC (checklist)

1. Leia abstract + introduction: pergunta científica / aplicação.
2. Localize descrição de paradigma MI / feedback.
3. Anote pipeline de sinal (filtros, features, classificador) — mesmo que parcialmente.
4. Veja como avaliam (métrica, sujeitos, sessões).
5. Extraia **limites** admitidos pelos autores.
6. Escreva 5 linhas: *o que eu reimplemento no synth* vs *o que exigiria estudo humano IRB*.


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

