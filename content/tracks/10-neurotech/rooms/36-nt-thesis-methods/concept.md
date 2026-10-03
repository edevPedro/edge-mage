# Conceito — Módulo de Métodos Reproduzíveis (Padrão MSc / Journal)

## 1. O Padrão de Reprodutibilidade em Neuroengenharia
A seção de **Métodos (*Methods*)** de uma dissertação de mestrado ou artigo científico em neurotecnologia deve ser redigida para um revisor cético e hostil: qualquer pesquisador independente no mundo deve conseguir replicar os resultados numéricos exatos a partir da descrição textual.

### Os Componentes Obrigatórios do Artefato (`study-log/artifacts/neuro-thesis-methods.md`)
O validador automatizado do curso audita a presença rigorosa dos seguintes campos estruturados:
1. **Dados (`data`)**: Especificação exata do dataset (ex: *BCI Competition IV Dataset 2a*, 9 sujeitos, 22 canais de EEG em $250\text{ Hz}$).
2. **Métricas (`metrics`)**: Coeficiente Kappa de Cohen ($\kappa$) e acurácia observada por sujeito, acompanhados da matriz de confusão e do cálculo da Taxa de Transferência de Informação de Wolpaw (ITR em bits/min).
3. **Limites e Salvaguardas Éticas (`limits`)**: Critérios objetivos de exclusão de ensaios com artefatos de amplitude ($>100\ \mu\text{V}$), limites de saturação e declaração de consentimento institucional/IRB.
4. **Número Derivado do Fundamento Físico**: Parâmetro quantitativo com unidade SI explícita (ex: taxa de amostragem $f_s = 250\text{ Hz}$, banda passante do biquad $8\text{--}12\text{ Hz}$, ou latência de inferência $T_{\text{inferência}} = 12.5\text{ ms}$).
5. **Reprodutibilidade Estrita (`reproducibility`)**: Sementes determinísticas de geradores pseudoaleatórios (`seed=42`), esquemas de particionamento contíguo em blocos (`split_blocked`) e versões das bibliotecas ([MNE-Python](https://mne.tools/stable/index.html) e [scikit-learn](https://scikit-learn.org/stable/user_guide.html)).

## 2. Modos de Falha Operacionais
1. **Ocultar Sementes e Parâmetros de Filtro**: Descrever "o sinal foi filtrado e classificado" sem especificar a ordem do filtro, as frequências de corte de 3 dB, a topologia (ex: Chebyshev vs Butterworth vs FIR linear-phase) e a semente de particionamento. Sem esses dados, o experimento é cientificamente irreprodutível.
2. **Reivindicar Validação Causal com Filtros Acausais**: Afirmar na metodologia que o algoritmo foi projetado para uso em tempo real enquanto o código executa `filtfilt` bidirecional ou normalização z-score com a média global da sessão inteira.

## 3. O que a Próxima Sala Assume
A sala seguinte ([`nt-research-project`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/37-nt-research-project/room.yaml)) assume que a metodologia está blindada e formalizada, executando o pipeline experimental completo para gerar os resultados que destravam a runa de pesquisa (`rune-neuro-research`).
