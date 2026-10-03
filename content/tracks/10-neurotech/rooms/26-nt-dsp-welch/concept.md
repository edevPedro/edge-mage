# Conceito — Densidade Espectral de Potência (PSD), Método de Welch e Vazamento Espectral

A estimação do conteúdo espectral de séries temporais biológicas não-estacionárias requer compromissos matemáticos entre resolução de frequência e redução de variância.

## 1. O Problema do Periodograma Bruto
Dado um sinal discreto $x[n]$ com $N$ amostras, o periodograma clássico é:
$$P_{xx}(f) = \frac{1}{N} \left| \sum_{n=0}^{N-1} x[n] e^{-j 2\pi f n} \right|^2$$
Para processos estocásticos estacionários, a variância do periodograma bruto não converge para zero quando $N \to \infty$: $\text{Var}(P_{xx}(f)) \approx P_{xx}^2(f)$. A estimativa é ruidosa e inconsistente.

## 2. O Método de Welch (Averaged Modified Periodogram)
O método proposto por Peter Welch divide o sinal de comprimento $N$ em $K$ segmentos de comprimento $L$, com sobreposição de $D$ amostras (geralmente 50%, $D = L/2$):
1. Cada segmento $x_k[n]$ é multiplicado por uma janela temporal $w[n]$ (ex. Hanning ou Hamming):
   $$\tilde{x}_k[n] = x_k[n] w[n], \quad n = 0, \dots, L-1$$
2. Calcula-se o periodograma modificado de cada segmento:
   $$I_k(f) = \frac{1}{L U} |\text{FFT}(\tilde{x}_k)|^2, \quad U = \frac{1}{L} \sum_{n=0}^{L-1} w^2[n]$$
3. A densidade espectral final é a média aritmética através dos $K$ segmentos:
   $$S_{xx}(f) = \frac{1}{K} \sum_{k=1}^K I_k(f)$$

A média reduz a variância da estimativa por um fator proporcional a $1/K$, proporcionando um espectro suave e estatisticamente confiável.

## 3. O Trade-Off de Resolução Espectral
A resolução em frequência de cada segmento é inversamente proporcional à sua duração temporal $T_{\text{seg}} = L / f_s$:
$$\Delta f = \frac{1}{T_{\text{seg}}} = \frac{f_s}{L}$$
- Segmentos longos (ex. $2\text{ s}$ a $250\text{ Hz}$, $L = 500$): Alta resolução ($\Delta f = 0.5\text{ Hz}$), mas poucos segmentos para mediar (maior variância).
- Segmentos curtos (ex. $0.5\text{ s}$, $L = 125$): Resolução mais grosseira ($\Delta f = 2\text{ Hz}$), mas muitos segmentos (baixa variância).

## 4. Modos de Falha na Prática de Engenharia
1. **Janela Retangular Implícita:** Usar FFT direta sem função de janelamento, provocando vazamento espectral severo onde harmônicos de rede elétrica vazam para a banda beta.
2. **Segmentos Excessivamente Curtos:** Usar janelas de 100 ms para estimar ondas delta (1 Hz), violando o critério fundamental de que a janela deve conter múltiplos ciclos completos da menor frequência de interesse.

## O Que a Próxima Sala Assume
A próxima sala (`nt-filter-design-depth`) — **FIR vs IIR e atraso de grupo** — compara filtros digitais de resposta finita (FIR) e infinita (IIR) sob critérios de linearidade de fase e atraso de grupo.

## Artigos de Apoio e Leituras Recomendadas
- [scipy.signal.welch](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Michel & Brunet EEG source imaging (OA)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
