# Conceito — Artefatos Fisiológicos e Rejeição por Limiar

Os sinais cerebrais de escalpo coexistem com fontes biológicas extracerebrais e ruídos ambientais cuja amplitude supera com frequência os biopotenciais corticais em várias ordens de magnitude.

## 1. As Principais Fontes de Contaminação
1. **Eletrooculograma (EOG - Piscadas e Movimentos Oculares):**
   - O olho funciona como um dipolo elétrico eletrostático permanente ($pprox 100\text{ mV}$).
   - Movimentos oculares e piscadas geram deflexões lentas ($0.5\text{--}4\text{ Hz}$) com amplitudes de $100\text{ a } 400\ \mu\text{V}$, concentradas nos canais frontais ($Fp1, Fp2, Fz$), mas irradiando até as regiões centrais.
2. **Eletromiograma (EMG - Atividade Muscular Craniana e Facial):**
   - Contrações de mandíbula, deglutição e tensão nos músculos temporal e occipital.
   - Espectro de alta frequência ($20\text{ a } >100\text{ Hz}$), com amplitudes que chegam a milivolts ($> 1000\ \mu\text{V}$), contaminando diretamente a banda beta e gama.
3. **Eletrocardiograma (ECG - Batimento Cardíaco):**
   - O complexo QRS do coração pode acoplar capacitivamente no escalpo, especialmente em eletrodos referenciados na orelha ou mastoide, gerando picos periódicos de $\approx 1\text{ Hz}$.
4. **Interferência Eletromagnética de Rede (50/60 Hz):**
   - Ruído harmônico de acoplamento capacitivo com a fiação do ambiente.

## 2. Estratégias de Rejeição de Artefatos
- **Rejeição por Limiar de Amplitude:** Ensaios cujo valor absoluto máximo exceda um limiar fisiológico (por exemplo, $|x| > 100\ \mu\text{V}$) são descartados imediatamente da calibração.
- **Detecção Estatística (Kurtosis / Variância):** Detecção de outliers em que a distribuição temporal se afasta de uma gaussiana estacionária.
- **Decomposição em Componentes Independentes (ICA):** Separação cega de fontes para subtrair o componente espacial do EOG preservando os canais cerebrais.

## 3. Modos de Falha na Prática de Engenharia
1. **Descarte Excessivo de Dados:** Definir um limiar agressivo demais (ex. $30\ \mu\text{V}$), eliminando ensaios normais de sujeitos com ritmos de grande amplitude.
2. **Confundir EMG com Ritmo Gama:** Assumir que atividade de $40\text{ Hz}$ observada em voluntários sob estresse é sinal neural, quando se trata de micro-contrações de tensão na testa.

## O Que a Próxima Sala Assume
A próxima sala (`nt-mi-paradigm`) — **Imagética motora (paradigma)** — estrutura o desenho temporal de épocas de calibração para tarefas cognitivas de imagética motora bimanual.

## Artigos de Apoio e Leituras Recomendadas
- [OpenBCI EEG Setup](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/) — *Documentação Técnica*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
- [Urigüen & Garcia-Zapirain — EEG artifact removal methods (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4462641/) — *Artigo Científico*: Leitura fundamental para fundamentar os conceitos teóricos e destravar a implementação técnica do laboratório.
