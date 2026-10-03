# Conceito — Estatística Inferencial em BCI, Chance Level e Testes de Permutação

A avaliação da performance em neurotecnologia exige rigor inferencial: pequenos tamanhos de amostra e não-estacionariedade dos biopotenciais tornam testes paramétricos convencionais (como t-Student não pareado) frequentemente inválidos.

## 1. O Nível de Acaso (Chance Level) Binomial
Em experimentos com número finito de ensaios $N$, o nível de acaso empírico não é a probabilidade teórica $1/K$. A probabilidade de obter $k$ acertos por puro acaso em $N$ ensaios com probabilidade basal $p = 1/K$ segue a distribuição binomial:
$$P(X = k) = \binom{N}{k} p^k (1 - p)^{N - k}$$

O limiar de significância estatística ao nível $\alpha$ (tipicamente $0.05$) é o menor valor $k_{\text{crit}}$ tal que:
$$P(X \ge k_{\text{crit}}) = \sum_{k=k_{\text{crit}}}^N \binom{N}{k} p^k (1 - p)^{N - k} \le \alpha$$
- Para $N = 20$ e $K = 2$, o limiar de significância a $5\%$ é $75\%$ de acurácia.
- Para $N = 100$ e $K = 2$, o limiar cai para $\approx 58\%$.
- Apenas quando $N \to \infty$, o limiar converge para $50\%$.

## 2. Testes de Permutação Não-Paramétricos
Em BCI, dados contíguos de EEG violam a premissa de observações independentes e identicamente distribuídas (i.i.d.). O teste de permutação constrói a distribuição nula empírica diretamente a partir dos dados:
1. Calcula-se a estatística observada $T_{\text{obs}} = \bar{S}_A - \bar{S}_B$.
2. Agrupam-se todas as observações e, a cada iteração, sorteiam-se aleatoriamente os rótulos de grupo.
3. Calcula-se a estatística permutada $T_p$.
4. O valor-p empírico é a fração das permutações onde $T_p \ge T_{\text{obs}}$:
   $$p = \frac{1 + \sum_{i=1}^P \mathbb{I}(T_i \ge T_{\text{obs}})}{1 + P}$$

## 3. Modos de Falha na Prática de Engenharia
1. **Comparações sem Ajuste de Tamanho Amostral:** Considerar 70% em 10 ensaios como "superior" a 60% em 200 ensaios.
2. **Ignorar Dependência Temporal:** Tratar janelas de tempo contíguas do mesmo trial como amostras independentes em testes estatísticos.

## O Que a Próxima Sala Assume
A próxima sala (`nt-hypothesis-power`) — **Hipótese, potência e múltiplos testes** — ensina o controle de taxa de falsas descobertas (FDR / Bonferroni) e o cálculo do poder estatístico em pipelines multicanais.

## Artigos de Apoio e Leituras Recomendadas
- [Lotte et al. JNE 2007 — classification review](https://doi.org/10.1088/1741-2560/4/2/R01) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Schlögl et al. JNE 2005 — κ / 4-class MI](https://doi.org/10.1088/1741-2560/2/4/L02) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
