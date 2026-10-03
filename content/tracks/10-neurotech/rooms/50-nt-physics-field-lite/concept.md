# Conceito — Decaimento de Campo Eletrostático e Profundidade de Fontes

A física da eletrostática quasistática governa a propagação e atenuação de potenciais bioelétricos gerados no encéfalo.

## 1. A Atenuação Geométrica Quadrática do Dipolo
Para um dipolo de corrente com momento $p$ em um meio condutor homogêneo, o potencial a uma distância $r$ é:
$$V(r) \propto \frac{1}{r^2}$$
A razão de potências entre uma fonte próxima ($r_{\text{near}}$) e uma fonte distante ($r_{\text{far}}$) é:
$$\frac{V_{\text{near}}}{V_{\text{far}}} = \left( \frac{r_{\text{far}}}{r_{\text{near}}} \right)^2$$
- Uma fonte ao dobro da distância gera um quarto ($1/4$) do potencial.
- Uma fonte a quatro vezes a distância gera apenas um dezesseis avos ($1/16$) do potencial.

## 2. Condução de Volume e Blindagem Óssea
Além da queda puramente geométrica:
- O osso craniano possui condutividade elétrica cerca de $80\times$ menor que o líquor e o tecido cerebral, atuando como um filtro passa-baixas espacial que espalha e atenua correntes profundas.
- Para estimar fontes com precisão volumétrica, são necessários modelos avançados de elementos finitos (FEM) ou camadas esféricas concêntricas (Boundary Element Method - BEM).

## 3. Modos de Falha na Prática de Engenharia
1. **Alegações de Decodificação Subcortical em EEG de Superfície:** Reivindicar que um algoritmo decodifica núcleos da base ou amígdala a partir de 8 canais de escalpo sem controle de artefatos.
2. **Ignorar Fontes Opostas:** Dipolos em paredes opostas do mesmo sulco cortical podem cancelar mutuamente seus campos a distância, gerando potencial zero no eletrodo superior.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-elec-opamp-noise`) analisa o ruído elétrico de amplificadores operacionais, ruído térmico Johnson e taxa de rejeição de modo comum (CMRR).

## 5. Ponto de Destrave do Lab
Consulte o tratamento clássico de propagação de campos e problemas diretos de EEG em [Nunez & Srinivasan (Electric Fields of the Brain, Oxford University Press)](https://global.oup.com/academic/product/electric-fields-of-the-brain-9780195050387).
