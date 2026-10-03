# História — A Frequência que Cega o Decodificador

Na bancada de processamento de sinais, uma equipe de desenvolvimento integra a cadeia de entrada de uma aplicação de BCI. O streamer de EEG alimenta o sistema com amostras digitalizadas a 250 Hz vindas de um voluntário realizando testes de imagética motora. O classificador em teste apresenta uma acurácia aparente de 92% na sessão matinal, mas quando os testes são repetidos na sala ao lado, a acurácia cai para 51% — exatamente o nível de puro acaso.

O engenheiro de sinais abre o analisador de Fourier e inspeciona o espectro dos canais brutos.

No meio do sinal cortical, uma espícula colossal de interferência de rede elétrica ergue-se exatamente em $60	ext{ Hz}$, com magnitude dez vezes superior a qualquer ritmo biológico. Na primeira sala de testes, o voluntário flexionava levemente o trapézio direito durante as instruções visuais, acoplando capacitivamente a corrente de $60	ext{ Hz}$ através do corpo de forma sincronizada com as classes do experimento. O algoritmo de machine learning não estava aprendendo ritmos cerebrais; estava aprendendo o zumbido da fiação elétrica modulado por tensão muscular.

— Se alimentarmos o classificador com o espectro bruto, ele sempre escolherá o caminho de menor resistência matemática: a fonte de maior energia, mesmo que seja ruído espúrio — adverte o engenheiro sênior. — Precisamos de duas etapas imediatas no pipeline digital: um filtro notch com fator de qualidade ajustado para atenuar estritamente os $60	ext{ Hz}$, e um banco de filtros passa-faixa (Filter Bank) que particione o espectro em gavetas fisiológicas isoladas, como a banda $\mu$ ($8	ext{--}12	ext{ Hz}$) e a banda $eta$ ($16	ext{--}24	ext{ Hz}$).

Eles projetam as seções de filtros digitais causais de segunda ordem (SOS) e aplicam a máscara seletiva sobre as bandas. Com a interferência eliminada e as faixas sensoriomotoras isoladas, o sinal biológico autêntico emerge limpo para a extração de características.
