# Conceito — Potenciais Evocados, Paradigma Oddball e o P300 Speller

## 1. O Paradigma Oddball de Farwell & Donchin (1988)
O P300 Speller é uma das interfaces cérebro-computador mais robustas e historicamente consagradas da neuroengenharia:
- **Estímulos Frequentes (Não-Alvo):** Flashes de linhas/colunas que não contêm o símbolo desejado pelo usuário (probabilidade $\sim 83\%$, ou $5/6$). Não provocam deflexões consistentes na média.
- **Estímulos Raros (Alvo):** Flashes da linha ou coluna contendo o símbolo alvo (probabilidade $\sim 17\%$, ou $1/6$).

## 2. A Onda P300 (P3b)
O componente P300 é uma deflexão positiva (*P* de positiva) endógena do sinal de EEG com as seguintes propriedades:
- **Latência:** Ocorre aproximadamente $300\text{ ms}$ após o estímulo sensorial, tipicamente distribuída no intervalo de $250\text{ a }450\text{ ms}$ dependendo da idade e atenção do sujeito.
- **Topografia:** Distribuição máxima sobre áreas parietais e centrais ao longo da linha média craniana ($Pz, Cz$).
- **Significado Cognitivo:** Reflete a atualização da memória operacional (*context updating*) e o reconhecimento de um evento relevante esperado.

## 3. Algoritmo de Extração de Pico em Épocas de ERP
Para um sinal de EEG segmentado relativo ao início do estímulo ($t = 0\text{ ms}$):
1. **Conversão de Tempo para Índices de Amostra:**
   Dado que a taxa de amostragem é $f_s$ (amostras/segundo):
   $$idx_{start} = \text{int}\left(\frac{start\_ms}{1000.0} \times f_s\right)$$
   $$idx_{end} = \text{int}\left(\frac{end\_ms}{1000.0} \times f_s\right)$$
2. **Busca do Máximo Positivo:**
   Na janela temporal $[idx_{start}, idx_{end}]$, determina-se o valor de amplitude máxima:
   $$V_{peak} = \max_{i = idx_{start}}^{idx_{end}} s[i]$$

## 4. O Que a Próxima Sala Assume
A próxima sala (`nt-case-berlin-mi`) conecta a decodificação de ritmos aos casos históricos publicados, explorando o benchmark Berlin BCI.
