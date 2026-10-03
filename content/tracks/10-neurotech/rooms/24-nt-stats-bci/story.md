# História — A Ilusão da Moeda Viciada

Em uma reunião de avaliação experimental, um pesquisador exibe com entusiasmo os resultados de uma nova técnica de extração de características testada em uma sessão rápida com um voluntário. O protocolo continha 20 ensaios de imagética motora (10 da mão direita e 10 da mão esquerda), e o classificador obteve 13 acertos — exatamente 65% de acurácia.

— Superamos a taxa de 50%! — afirma o pesquisador. — Temos evidência de que a modulação neural foi decodificada.

A bioestatística sênior do laboratório balança a cabeça negativamente e abre uma simulação no terminal:
— Em uma amostra pequena de apenas 20 ensaios, a hipótese nula de que o classificador está apenas adivinhando aleatoriamente não se comporta como uma constante em 50% — adverte ela. — A distribuição de acertos sob pura adivinhação aleatória segue uma distribuição binomial $B(n=20, p=0.5)$. Vamos calcular a probabilidade acumulada de obter 13 ou mais acertos puramente por sorte.

Ela executa a conta: a probabilidade de obter 13 ou mais acertos em 20 lançamentos de uma moeda honesta é de aproximadamente 13.1% ($p = 0.131$). Como esse valor é muito superior ao nível de significância padrão $\alpha = 0.05$, o resultado de 65% não tem relevância estatística alguma: é compatível com o acaso.

— Para 20 ensaios com $\alpha = 0.05$, o limiar exato de chance level é de 15 acertos (75%) — demonstra a bioestatística. — Para avaliar rigorosamente se dois pipelines de decodificação são genuinamente diferentes sem fazer suposições irreais de normalidade dos dados, nós utilizamos o teste de permutação não-paramétrico: embaralhar os rótulos dezenas de milhares de vezes e medir quantas vezes a diferença simulada supera a diferença observada.

O pesquisador programa a rotina de teste de permutação (`permutation_p_value`). Compreendendo a volatilidade estatística de pequenos tamanhos amostrais, ele amplia o protocolo para 120 ensaios balanceados, onde as verdadeiras diferenças fisiológicas emergem com suporte estatístico incontestável.
