# Conceito — Potenciais Evocados Visuais de Estado Estável (SSVEP) e Análise Harmônica

O SSVEP é um paradigma exógeno de BCI baseado na resposta de arrasto eletrofisiológico do córtex visual a estímulos luminosos periódicos.

## 1. Biofísica do SSVEP
Quando o sistema visual é estimulado por uma fonte intermitente piscando a uma frequência $f_0$ (tipicamente na faixa de $8\text{--}30\text{ Hz}$):
- Os potenciais pós-sinápticos em V1 e áreas extraestriadas sincronizam-se na frequência fundamental $f_0$.
- Devido à não-linearidade da transdução retiniana e do circuito cortical, harmônicos de ordem superior ($2 f_0, 3 f_0, \dots$) aparecem com amplitudes mensuráveis no escalpo occipital ($Oz, O1, O2$).

## 2. Métodos de Detecção Espectral
1. **Detecção por Razão Espectral (Signal-to-Noise Ratio - SNR):**
   Compara-se a potência na frequência de interesse $P(f_0)$ contra a média das frequências vizinhas $P_{\text{noise}}$:
   $$\text{SNR}(f_0) = \frac{P(f_0)}{\frac{1}{2\Delta f} \left[ \int_{f_0 - \Delta f}^{f_0 - \delta} P(f)df + \int_{f_0 + \delta}^{f_0 + \Delta f} P(f)df \right]}$$
   Se a potência relativa superar um limiar predefinido, a classe correspondente é ativada.
2. **Análise de Correlação Canônica (CCA):** Método multi-canal avançado que encontra combinações lineares espaciais que maximizam a correlação entre os sinais de EEG e ondas senoidais puras de referência nas frequências dos alvos.

## 3. Modos de Falha na Prática de Engenharia
1. **Fadiga Visual e Risco de Fotossensibilidade:** Estímulos de alta luminância abaixo de 15 Hz podem causar cansaço ocular rápido e representam risco formal de desencadear crises em indivíduos com epilepsia fotossensível (triagem médica obrigatória).
2. **Harmônicos Compartilhados:** Utilizar alvos em $10\text{ Hz}$ e $20\text{ Hz}$, onde o 2º harmônico do primeiro confunde-se com a frequência fundamental do segundo.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-fbcsp-bakeoff`) é a eletiva de comparação competitiva (bake-off) entre Filter Bank CSP e Classificadores Riemannianos no mesmo dataset.

## 5. Ponto de Destrave do Lab
Consulte a revisão abrangente de SSVEP em [Zhu et al. (IEEE Trans Biomed Eng 2010, High-speed BCI based on SSVEP)](https://doi.org/10.1109/TBME.2010.2041352) e [Lin et al. (J Neural Eng 2006)](https://doi.org/10.1088/1741-2560/3/4/007).
