# Conceito — Ética, consentimento e limites do BCI educacional

Este círculo ensina literacia e labs seguros. **Não** ensina produto clínico, “leitura da mente”, implant DIY nem vigilância.

## Belmont (âncora prática)

O [Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/index.html) resume três princípios que o curso traduz para BCI educacional:

| Princípio | Em BCI / EEG | Pergunta de checklist |
|-----------|--------------|------------------------|
| **Respeito pelas pessoas** | Autonomia + proteção de quem tem autonomia reduzida | Houve consentimento informado *antes* de gravar? Pode recusar sem castigo? |
| **Beneficência** | Maximizar benefício / minimizar dano; honestidade sobre incerteza | O benefício prometido é proporcional à evidência? Riscos (cansaço, estigma, leak de dados) foram ditos? |
| **Justiça** | Distribuição equitativa de riscos e benefícios | Quem treina o modelo? Quem é classificado? Quem lucra com o pitch? |

Belmont **não** é um protocolo IRB completo — é o vocabulário mínimo antes de qualquer sala com “sujeito humano” eletivo.

## Consentimento informado (template mental)

Antes de EEG humano *eletivo* (não obrigatório neste MVP), o sujeito deve entender, em linguagem clara:

1. **O quê** será medido (EEG de escalpo; canais; duração aproximada).
2. **Para quê** (treino educacional / pesquisa definida — não “ler pensamentos”).
3. **Riscos** razoáveis (desconforto do gel/cap, fadiga, possível identificação se dados forem mal anonimizados).
4. **Benefícios** honestos (aprendizado; contribuição a dataset *se* acordado) — sem milagre terapêutico.
5. **Voluntariedade** e direito de parar.
6. **Dados**: quem guarda, por quanto tempo, se há partilha, como anonimizar.
7. **Contacto** para dúvidas (responsável do lab / curso).

MVP do círculo: preferir **dados sintéticos** ou **datasets abertos citados** (ex. competições / papers OA) até haver contexto ético real.

## Neurorights e overclaim

Ienca & Andorno ([PMC5447102](https://pmc.ncbi.nlm.nih.gov/articles/PMC5447102/), DOI [10.1186/s40504-017-0050-1](https://doi.org/10.1186/s40504-017-0050-1)) discutem direitos emergentes na era da neurotecnologia (privacidade mental, liberdade cognitiva, etc.). Para este curso, a tradução operacional é:

- **Não** vender EEG de escalpo como acesso ao conteúdo semântico do pensamento.
- **Não** treinar pipelines para vigilância não consentida (RH, salas de aula sem opt-in, etc.).
- **Sim** discutir limites: MI/ERD ≠ “ler intenção verbal”; κ alto em synth ≠ desempenho clínico.

**Overclaim** = afirmar capacidade que o sinal / o desenho experimental / a validação **não** sustentam. Exemplos proibidos no discurso do círculo:

- “Lê pensamentos / memórias / mentiras.”
- “Diagnostica doença X a partir do MVP estudantil.”
- “Controle remoto do cérebro” via filtro-banco didático.

## Dual-use literacy (sem receita)

Alfabetização dual-use aqui significa:

- Reconhecer que interfaces neurais e classificadores *podem* ser desviados (perfilamento, coerção, weaponização em sentido amplo).
- Discutir salvaguardas: consentimento, minimização de dados, transparência de limites, revisão ética.
- **Zero** procedimentos ofensivos, zero “como burlar consentimento”, zero design de arma.

UNESCO — *Recommendation on the Ethics of AI* (2021) reforça proporcionalidade, privacidade e supervisão humana; use como leitura de contexto, não como checklist clínico.

## Offline vs online e responsabilidade

- **Offline**: replay / treino — ainda exige ética se dados forem humanos; synth reduz risco.
- **Online**: latência e feedback fecham o laço com a pessoa — erro + overclaim = dano psicossocial potencial (frustração, falsa esperança). Orçamento de latência não des Culpa ética.

## O que este curso *é* e *não é*

| É | Não é |
|---|--------|
| Literacia MSc-prep + labs com emuladores | Curso de certificação clínica |
| Papers abertos / DOI como âncora | Reprodução bit-a-bit de produto comercial |
| Dual-use *awareness* | Manual de abuso |
| Rota Neural a Mago Supremo | Atalho sem Estuda |
