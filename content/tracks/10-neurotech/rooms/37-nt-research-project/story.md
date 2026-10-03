# História — A Execução do Pipeline Experimental

No laboratório de computação de alto desempenho, um pesquisador prepara a execução automatizada de seu miniprojeto de pesquisa quantitativo. Meses de estudo de fundamentos biofísicos, circuitos analógicos, processamento digital de sinais e machine learning convergem para este instante: rodar o pipeline completo ponta a ponta sobre a base aberta de BCI e gerar o relatório experimental consolidado.

Ele abre o script de execução e conecta os módulos integrados:
1. **Módulo de Ingestão:** Carregamento de dados de múltiplos voluntários do PhysioNet EEGBCI.
2. **Módulo de Filtragem:** Filtro passa-faixa causal Butterworth de 4ª ordem ($8\text{--}30\text{ Hz}$) com filtro notch em 60 Hz.
3. **Módulo Espacial e Decodificação:** Decomposição em Padrões Espaciais Comuns (CSP) com 4 filtros espaciais, acoplada ao Discriminante Linear com regularização de encolhimento de Ledoit-Wolf.
4. **Validação Cruzada Hermética:** 5-fold em blocos de ensaios completos (`BlockKFold`), garantindo zero vazamento de dados.

O pesquisador executa o pipeline através da função `run_bci_pipeline_eval`:
O console processa centenas de ensaios de calibração e teste. Ao final da execução, o relatório de telemetria exibe os resultados consolidados:
- Acurácia média observada: $78.4\%$.
- Coeficiente Kappa de Cohen médio: $\kappa = 0.568$ (rejeição categórica da hipótese nula com $p < 0.001$).
- Latência média de decisão por janela: $4.2\text{ ms}$.
- Concessão da Runa de Pesquisa (`rune-neuro-research`).

A coordenadora científica revisa os logs e assina a homologação:
— Este é o padrão de excelência da neuroengenharia real. Você não apenas desenhou uma proposta teórica; você implementou, testou, auditou e comprovou que seu sistema é computacionalmente determinístico e estatisticamente inatacável.
