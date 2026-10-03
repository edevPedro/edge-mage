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

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-features-bandpower`) aborda a extração matemática da potência de banda em canais limpos como a principal característica para classificadores lineares.

## 5. Ponto de Destrave do Lab
Para estudar métodos formais de rejeição e correção de artefatos em EEG, consulte a revisão de [Urigüen & Garcia-Zapirain (J Neural Eng 2015, PMC4605434)](https://doi.org/10.1088/1741-2560/12/3/031001) e as diretrizes do [MNE-Python Artifact Correction](https://mne.tools/stable/auto_tutorials/preprocessing/20_rejecting_bad_data.html).
