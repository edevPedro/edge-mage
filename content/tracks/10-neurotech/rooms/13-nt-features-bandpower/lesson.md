# Lição — Potência de Banda (Bandpower) e Extração de Features

## 1. Do Sinal Filtrado às Características Discriminantes
1. **Potência Média de Janela**:
   $$P = \frac{1}{N} \sum_{n=0}^{N-1} x[n]^2$$
   Representa a energia média por amostra na banda isolada pelo filtro biquad.

2. **Compressão Logarítmica de Faixa Dinâmica**:
   $$f = \log_{10}(P)$$
   Simetriza a distribuição e aproxima o espaço de features da hipótese de normalidade multivariada necessária para o classificador LDA.

3. **Assimetria Contralateral em Imagética Motora**:
   - Imagética da Mão Direita $\implies$ Ativação do córtex motor esquerdo $\implies$ Dessincronização do ritmo mu em C3 ($P_{C3} \downarrow \implies \log P_{C3} < \log P_{C4}$).
   - Imagética da Mão Esquerda $\implies$ Ativação do córtex motor direito $\implies$ Dessincronização do ritmo mu em C4 ($P_{C4} \downarrow \implies \log P_{C4} < \log P_{C3}$).

## 2. As Funções de Laboratório Desta Sala
- `bandpower(xs)`: Computa a média dos quadrados das amostras em um ensaio.
- `log_bandpower_2ch(trial_c3, trial_c4)`: Extrai o vetor de features normalizado $[\log_{10}(P_{C3}), \log_{10}(P_{C4})]$, validando a positividade estrita da energia para evitar colapso numérico.

Para destravar o lab, abra [Padfield et al. (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) e leia como Padfield trata bandpower de MI (mu/beta, janela versus baseline) para fechar a feature antes do classificador.
