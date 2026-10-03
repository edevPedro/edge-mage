# Conceito — Orçamento de Latência em Malha Fechada (Closed-Loop Latency Budget)

Em interfaces cérebro-computador interativas e neuropróteses, a latência de ponta a ponta determina a estabilidade do sistema e a sensação psicológica de agência do usuário.

## 1. As Três Etapas do Orçamento de Latência
O tempo total transcorrido entre a geração do biopotencial no córtex e a ação no mundo físico divide-se em:
$$t_{\text{total}} = t_{\text{sense}} + t_{\text{decide}} + t_{\text{act}}$$

1. **Sensoriamento ($t_{\text{sense}}$):**
   - Duração da janela temporal de amostras acumuladas necessária para o algoritmo extrair características estáveis ($t_{\text{window}}$).
   - Atraso de grupo introduzido pelos filtros digitais causais ($t_{\text{filter}}$).
2. **Decisão / Decodificação ($t_{\text{decide}}$):**
   - Tempo de processamento do firmware ou software para aplicar filtros espaciais, calcular potências e executar o classificador ($t_{\text{compute}}$).
3. **Atuação ($t_{\text{act}}$):**
   - Transmissão de pacotes via barramento serial/BLE, decodificação no controlador robótico e resposta inercial mecânica dos motores ($t_{\text{mechanical}}$).

## 2. O Critério de Deadline Rígido
Para que o controle em malha fechada seja percebido como simultâneo e evite instabilidade oscilatória:
$$t_{\text{total}} \le t_{\text{deadline}}$$
- **Deadline clássico de usabilidade:** $150\text{--}200\text{ ms}$.
- **Aplicações de neuroestimulação rápida:** $< 40\text{ ms}$.
- Se $t_{\text{total}} > t_{\text{deadline}}$, ocorre uma **violação de deadline (deadline miss)**.

## 3. O Trade-Off Fundamental de Engenharia
Existe um conflito matemático inerente entre:
- **Resolução Espectral:** Janelas temporais longas ($1\text{--}2\text{ s}$) fornecem estimativas de frequência nítidas ($\Delta f = 1/T$), mas injetam latência inaceitável para controle rápido.
- **Latência de Resposta:** Janelas curtas ($100\text{--}250\text{ ms}$) respondem rapidamente, mas possuem resolução de frequência grosseira e maior variância estocástica.

## O Que a Próxima Sala Assume
A próxima sala (`nt-online-stub`) — **Loop online simulado** — integra o loop de simulação online contínuo com janelas temporais deslizantes e emissão assíncrona de predições.

## Artigos de Apoio e Leituras Recomendadas
- [Singh et al. — MI-BCI review (online challenges context, PMC8003721)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Ramsey et al. — Brain–computer interfaces in paralysis (review OA via PMC search)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3497935/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [OpenBCI docs](https://docs.openbci.com/) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
