# Conceito — Dipolo de Corrente e Atenuação Geométrica no Escalpo

O sinal capturado por eletrodos de EEG não é o potencial de ação de um neurônio isolado, mas a soma coerente de potenciais pós-sinápticos de dezenas de milhares de neurônios piramidais alinhados perpendicularmente às camadas corticais. Essa população em sincronia é biofisicamente modelada como um **dipolo de corrente**.

## 1. O Fundamento Físico do Lab

### O Potencial de Dipolo
Para um dipolo com momento dipolar $p$ (Ampère-metro ou Coulomb-metro) orientado em um ângulo $\theta$ em relação à normal, a uma distância $r$ em um meio condutor:
$$V(r, \theta) = \frac{p \cos\theta}{4\pi \epsilon_0 r^2}$$

### A Queda com o Quadrado da Distância ($1/r^2$)
Ao contrário de uma carga pontual monopolar (que cai com $1/r$), o potencial dipolar decai com o **inverso do quadrado da distância** ($1/r^2$):
- Na superfície cortical (eletrocorticografia / ECoG, $r_{\text{near}} \approx 1.5\text{ cm}$ do centro da fonte ativa):
  $$V_{\text{near}} \propto \frac{1}{0.015^2} \approx 4444$$
- No eletrodo de escalpo (passando por líquor, osso craniano e couro cabeludo, $r_{\text{scalp}} \approx 3.5\text{ cm}$):
  $$V_{\text{scalp}} \propto \frac{1}{0.035^2} \approx 816$$
- Apenas a distância geométrica pura reduz o potencial por um fator de $(35/15)^2 \approx 5.44$.
- Quando somamos a altíssima resistividade do osso craniano ($\approx 80\times$ mais resistivo que o córtex), o sinal é atenuado em dezenas a centenas de vezes, explicando por que potenciais corticais de milivolts viram microvolts discretos no escalpo.

## 2. Unidades e Grandezas
- **Momento dipolar ($p$):** $\text{A}\cdot\text{m}$ (corrente) ou $\text{C}\cdot\text{m}$.
- **Distância ($r$):** Metros ($\text{m}$).
- **Ângulo ($\theta$):** Radianos.
- **Potencial ($V$):** Volts ou microvolts.

## 3. Modo de Falha na Engenharia
Supor que um eletrodo mede apenas o que está milimetricamente abaixo dele. Se o dipolo estiver orientado tangencialmente (como nas paredes dos sulcos corticais), $\cos(\pi/2) = 0$: o eletrodo diretamente acima da fonte lê potencial zero, enquanto dois eletrodos distantes leem potenciais opostos (dipolo tangencial bipolar).

## O Que a Próxima Sala Assume
A próxima sala (`nt-physics-rc-tissue`) — **Physics — Tecido como RC (lite)** — modela os tecidos cranianos e a membrana celular como uma rede resistivo-capacitiva (RC) com constante de tempo característica.

## Artigos de Apoio e Leituras Recomendadas
- [EEG MI techniques (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6471241/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Michel & Brunet — EEG source imaging (PMC review)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6700197/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
