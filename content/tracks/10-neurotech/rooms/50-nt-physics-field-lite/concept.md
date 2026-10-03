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

## O Que a Próxima Sala Assume
A próxima sala (`nt-elec-circuit-fundamentals`) — **Elétrica — Ohm, Kirchhoff, DC/AC** — inicia a base de eletrônica analógica aplicando leis de Ohm e Kirchhoff na instrumentação de biopotenciais.

## Artigos de Apoio e Leituras Recomendadas
- [Michel & Brunet EEG source imaging OA](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
