# Conceito — Vetores, Projeção Espacial e Normalização de Energia

Em neuroengenharia computacional, um vetor $x \in \mathbb{R}^C$ representa uma amostra instantânea capturada simultaneamente através de $C$ canais de eletrodos (por exemplo, $[C_3, C_z, C_4]$ em microvolts, $\mu\text{V}$) ou um vetor de potências de banda espectral extraído de uma janela temporal.

## 1. O Fundamento Matemático do Lab

### Produto Interno como Filtragem Espacial
A operação fundamental que conecta eletrofisiologia a aprendizado de máquina é o produto interno $\langle w, x \rangle = w^T x = \sum_{i=1}^C w_i x_i$.
Geometricamente, essa operação projeta o vetor multicanal $x$ sobre a direção definida pelo vetor de pesos espaciais $w$:
- Se $w = [1, -1]^T$, o produto calcula a diferença bipolar entre dois eletrodos adjacentes ($V_{C3} - V_{Cz}$), rejeitando modo comum.
- Se $w$ é derivado de um algoritmo como CSP (Common Spatial Patterns) ou LDA, ele atua como um filtro espacial linear direcionado a maximizar a discriminação de tarefas motoras.

### Norma Euclidiana e Preservação de Escala
A norma euclidiana $L_2$ mede o comprimento ou a energia do vetor no espaço euclidiano:
$$\|w\|_2 = \sqrt{\sum_{i=1}^C w_i^2}$$

Para que um filtro espacial preserve a escala física do sinal sem injetar ganho espúrio nem atenuar arbitrariamente a amplitude bioelétrica, o vetor de pesos deve ser estritamente unitário ($\|w\|_2 = 1.0$):
$$\hat{w} = \frac{w}{\|w\|_2}$$

Se $\|w\|_2 = 0$, a projeção colapsa para zero absoluto em todas as dimensões, o que indica um vetor nulo degenerado que deve levantar `ValueError`.

## 2. Unidades e Grandeza Física
- **Potencial elétrico multicanal ($x$):** $\mu\text{V}$ (microvolts, tipicamente na faixa de $5\text{--}100\ \mu\text{V}$ em EEG de escalpo).
- **Pesos do filtro espacial ($w$):** Adimensionais ou inverso de impedância relativa.
- **Energia do sinal resultante ($\|x\|_2^2$):** $\mu\text{V}^2$.

## 3. Modos de Falha na Prática de Engenharia
1. **Filtro Espacial Não Normalizado:** Se o desenvolvedor projeta pesos espaciais (por exemplo, $w = [12.0, -8.0, 4.0]$) e esquece de normalizar por $\|w\|_2$, o sinal filtrado sofrerá uma amplificação linear descontrolada ($\times \sqrt{224} \approx 14.96$), saturando conversores subsequentes e descalibrando o bias $b$ do classificador linear.
2. **Canais em Escalas Heterogêneas:** Se um canal estiver medindo em milivolts (eletrooculograma) e outro em microvolts (EEG cortical), o produto interno será totalmente dominado pelo canal de maior magnitude, tornando os demais canais matematicamente invisíveis.

## 4. O que a Próxima Sala Assume
A sala seguinte ([`nt-math-matrices`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/44-nt-math-matrices/room.yaml)) assume que você compreende a projeção linear vetorial para organizar sequências de amostras na matriz de dados $X \in \mathbb{R}^{C \times T}$ e calcular a matriz de covariância amostral $\Sigma = \frac{1}{T-1} X X^T$.

## 5. Ponto de Destrave do Lab
Se a sua implementação falhar na normalização com divisões por zero ou dimensões incompatíveis, consulte a documentação oficial da álgebra linear de arrays no [NumPy linalg norm](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html) e a fundamentação geométrica de projeções lineares no [Khan Academy Vectors and Spaces](https://www.khanacademy.org/math/linear-algebra/vectors-and-spaces).
