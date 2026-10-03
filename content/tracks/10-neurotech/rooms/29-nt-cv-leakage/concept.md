# Conceito — Validação Cruzada em Blocos e a Ilusão do Vazamento de Dados (Data Leakage)

## 1. Fundamento Metodológico: A Barreira Epistêmica de Treino
Na decodificação de séries temporais biológicas (EEG), o erro metodológico mais devastador e comum em machine learning é o **vazamento de dados (*data leakage*)**, também denominado na literatura científica de análise circular ou *double dipping*.

O problema foi formalizado por [Gael Varoquaux et al. (NeuroImage 2017)](https://doi.org/10.1016/j.neuroimage.2016.10.038) e detalhado para BCIs por [Lotte et al. (DOI 10.1088/1741-2560/4/2/R01)](https://doi.org/10.1088/1741-2560/4/2/R01).

### O Mecanismo da Ilusão de Acerto em Ruído Puro
Considere um experimento sintético com $N = 40$ ensaios de ruído gaussiano puramente aleatório $\mathcal{N}(0, 1)$ contendo $D = 15$ features irrelevantes, rotulados aleatoriamente com classes $y \in \{0, 1\}$ (20 ensaios por classe). Como os dados são ruído puro, qualquer classificador honesto DEVE obter acurácia ao acaso ($\sim 50\%$).

Entretanto, observe o que acontece se o pipeline cometer **vazamento por seleção circular de features**:
1. O desenvolvedor seleciona as melhores features calculando a correlação ou separabilidade com os rótulos $y$ usando **todos os 40 ensaios** (treino e teste combinados).
2. Ele descobre, por mera flutuação estatística aleatória, duas variáveis que correlacionam ligeiramente com os rótulos.
3. Ele então separa os 10 ensaios de teste e treina um classificador linear nos outros 30 usando as features pré-selecionadas.
4. **Resultado**: O modelo atinge acurácia inflada de $80\%\text{--}90\%$ no teste! O teste não era independente: os rótulos do teste já haviam influenciado a escolha das variáveis no passo 1.

### O Princípio da Barreira de Treino e Split em Blocos
Para garantir validade científica e reprodutibilidade:
1. **Split Primeiro**: O conjunto de teste $\mathcal{D}_{\text{test}}$ é isolado imediatamente antes de qualquer cálculo estatístico.
2. **Transformações Estritamente no Treino**:
   Qualquer parâmetro $\theta$ (média, desvio padrão, ranking de features, matrizes espaciais CSP) é estimado unicamente em $\mathcal{D}_{\text{train}}$:
   $$\theta_{\text{train}} = f(\mathcal{D}_{\text{train}})$$
   E aplicado de forma puramente determinística sobre $\mathcal{D}_{\text{test}}$:
   $$\hat{x}_{\text{test}} = g(x_{\text{test}}; \theta_{\text{train}})$$
3. **Divisão em Blocos Contíguos (*Blocked Cross-Validation*)**:
   Em EEG contínuo, ensaios adjacentes compartilham autocorrelação temporal e estados lentos de impedância e fadiga. A divisão aleatória tradicional (*Random K-Fold*) vaza dependência temporal entre amostras vizinhas. Deve-se empregar partição contígua em blocos de ensaios inteiros (*Blocked Split*).

## 2. Modos de Falha Operacionais
1. **Fatiar uma Época Contínua em Janelas de 500 ms e Aplicar K-Fold Aleatório**: Se um ensaio de 4 segundos de imagética motora for fatiado em 8 janelas de 500 ms com overlap de $50\%$, e essas janelas forem embaralhadas aleatoriamente no K-Fold, janelas idênticas do mesmo ensaio cairão simultaneamente no treino e no teste. A acurácia sobe para $>95\%$, mas o sistema colapsa completamente para $50\%$ em tempo real com novos sujeitos.
2. **Otimizar Regularização no Fold de Teste**: Selecionar o parâmetro de encolhimento (*shrinkage*) $\gamma$ do LDA olhando para a acurácia do fold de teste externo. A seleção de hiperparâmetros requer validação cruzada aninhada (*Nested CV*) estritamente no loop interno.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-decode-mvp`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/14-nt-decode-mvp/room.yaml)) assume que você sabe particionar ensaios em blocos de treino e teste blindados contra vazamento, e utiliza os vetores de features bidimensionais $[\log_{10}(P_{C3}), \log_{10}(P_{C4})]$ de treino para calcular o hiperplano ótimo do Discriminante Linear Regularizado de Fisher (Shrinkage LDA).
