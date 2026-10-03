# Conceito — A Cadeia Sistêmica de Neuroengenharia

Uma Interface Cérebro-Computador (BCI) não é um problema isolado de machine learning. Ela é um sistema ciber-físico fechado que une eletrofisiologia, instrumentação analógica de microvolts, processamento digital de sinais em tempo real e controle adaptativo.

## 1. O Fundamento Biofísico e Sistêmico
O sinal de EEG de escalpo é a manifestação macroscópica de correntes pós-sinápticas integradas através de milhares de neurônios piramidais alinhados perpendicularmente ao córtex. O sinal sofre atenuação severa ao atravessar líquor, crânio e couro cabeludo, emergindo na superfície como potenciais de ordem de $10\text{--}100\ \mu\text{V}$.

A cadeia completa de aquisição e processamento compreende:
1. **Biofísica do Tecido:** Geração de dipolos de corrente e condução de volume.
2. **Interface Eletrodo-Pele:** Transdução iônico-eletrônica e impedância de contato.
3. **Front-End Analógico (AFE):** Amplificador de instrumentação, filtros anti-aliasing e rejeição de modo comum (CMRR).
4. **Digitalização e Firmware:** ADC de alta resolução (24-bit), amostragem determinística via DMA e empacotamento em buffers circulares.
5. **Processamento Digital de Sinais (DSP):** Banco de filtros passa-faixa, rejeição de artefatos e fatiamento temporal de epochs.
6. **Extração de Características e Decodificação:** Potência espectral de banda, geometria Riemanniana e modelos lineares regulares.
7. **Atuação e Malha Fechada:** Envio de comandos sob um orçamento rígido de latência ($< 150\text{ ms}$).

## 2. Unidades e Ordens de Grandeza
- **Biopotenciais de escalpo:** $10\text{--}100\ \mu\text{V}$ (microvolts).
- **Ruído térmico Johnson-Nyquist:** $\approx 1\ \mu\text{V}_{\text{RMS}}$ para eletrodos de $5\text{ k}\Omega$.
- **Relação Sinal-Ruído (SNR):** Tipicamente negativa ($-5\text{ a } -15\text{ dB}$) antes da filtragem espacial e temporal.
- **Taxa de amostragem padrão:** $250\text{--}1000\text{ Hz}$.

## 3. Modos de Falha na Prática de Engenharia
1. **Ilusão de Decodificação por Artefato:** Treinar modelos complexos sobre dados brutos onde o classificador aprende o reflexo de piscada ocular (EOG de $200\ \mu\text{V}$) ou contração de mandíbula (EMG de alta frequência) em vez do ritmo neural.
2. **Ignorar Latência e Causalidade:** Utilizar filtros não-causais bidirecionais (como `scipy.signal.filtfilt`) no treinamento offline e descobrir no hardware em tempo real que o algoritmo exige dados do futuro, tornando o sistema inoperante.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-ethics-consent`) estabelece o arcabouço ético formal e os limites de segurança e privacidade biométrica indispensáveis antes de qualquer coleta de dados em voluntários humanos.

## 5. Ponto de Destrave do Lab
Para compreender a visão panorâmica de uma cadeia completa de BCI e seus desafios reais, consulte a revisão abrangente de [Singh et al. (Sensors 2021, PMC8003721)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8003721/).
