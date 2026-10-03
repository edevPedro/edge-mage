# Conceito — Ritmos EEG e imagética motora

## Faixas clássicas (pedagógicas)

Bordas variam na literatura; memorize o suficiente para **escolher um filtro**.

| Ritmo | Hz (aprox.) | Onde / intuição | Uso neste círculo |
|-------|-------------|-----------------|-------------------|
| Delta | 0.5–4 | lento / sono | raramente feature MI |
| Theta | 4–8 | sonolência / memória (contexto) | cuidado com artefato / estado |
| Alfa | 8–12 | olhos fechados, occipital | ≠ mu só porque a banda se sobrepõe |
| **Mu** | ~8–12 | córtex **sensorimotor** | âncora MI / SMR |
| **Beta** | 13–30 | sensorimotor; frequentemente **ERD↓** em MI | banco de filtros com mu |
| Gama | >30 | rápido; difícil e ruidoso no escalpo | avançado; anti-alias importa |

**SMR (sensorimotor rhythm):** linguagem clássica para ritmos mu/beta ligados a córtex motor/sensorial — base de muitos BCIs não invasivos de MI. **Não** é “ler a mente”: é mudança de potência espectral correlacionada a tarefa de imagética / movimento.

## ERD / ERS (convenção do curso)

- **ERD (event-related desynchronization):** **queda** de potência numa banda após evento / durante tarefa (em MI, tipicamente mu/beta).
- **ERS:** **aumento** de potência (ex. rebound pós-movimento).

Erro comum de novato: “beta ativo = potência sobe”. Em MI, a convenção pedagógica deste curso é **ERD↓** em mu/beta durante imagética (detalhes e exceções na literatura — Pfurtscheller).

## MI → canais

Imagética de mão esquerda/direita modula, em média, ritmos sobre áreas motoras contralaterais (aproximação 10–20: **C3 / C4**). Volume conduction mistura fontes — física/blur explicam por que um canal não é “um neurónio”.

## Synth honesty

Emuladores com contraste de band-energy ensinam o **pipeline** (filtrar → potência → classificar). **Synth ≠ ERD fisiológico.** Não cite κ de synth como evidência clínica.

## Leituras âncora

- Pfurtscheller & Lopes da Silva — ERD/ERS DOI [10.1016/S1388-2457(99)00141-8](https://doi.org/10.1016/S1388-2457(99)00141-8)
- Padfield et al. [PMC6471241](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/)
- Singh et al. [PMC8003721](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/)

Isto **não** é diagnóstico clínico.


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

