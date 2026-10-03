# Conceito — Módulo de Artigo Científico Padrão Mestrado (Paper Module MSc)

## 1. O Padrão de Reprodução e Crítica Científica
O módulo de artigo científico de nível de mestrado (*Paper Module MSc*) estabelece o patamar de maturidade acadêmica do estudante de neuroengenharia: ir além da aceitação passiva das conclusões de um artigo publicado e dissecar sua cadeia metodológica, reproduzindo quantitativamente seus resultados e identificando suas fragilidades técnicas.

### Os Campos Obrigatórios do Artefato (`study-log/artifacts/neuro-paper-module-msc.md`)
O validador automatizado do sistema exige a presença explícita dos seguintes pilares estruturados:
1. **Identificador Estável (`doi`)**: O DOI oficial do artigo selecionado da lista canônica da especificação (ex: [Barachant et al. 2012, DOI 10.1109/TBME.2011.2172210](https://doi.org/10.1109/TBME.2011.2172210) sobre geometria Riemanniana, ou [Singh et al. 2021, DOI 10.3390/s21062173](https://doi.org/10.3390/s21062173) sobre desafios online).
2. **Dados (`data`)**: Descrição da base experimental (ex: *BCI Competition IV Dataset 2a*, sujeitos, canais e condições experimentais).
3. **Métricas (`metrics`)**: Comparação quantitativa explícita entre a métrica reportada pelos autores originais e o valor reproduzido no código independente:
   $$\Delta = \text{Métrica}_{\text{reproduzida}} - \text{Métrica}_{\text{publicada}}$$
4. **Limites e Crítica Estruturada (`limits` e `critique`)**: Exame de potenciais armadilhas (risco de vazamento de dados, complexidade computacional para hardware embarcado, generalização inter-sujeitos e limites éticos de consentimento).
5. **Fatia de Métodos (`methods_slice`)**: Transcrição concisa e código correspondente do núcleo algorítmico reproduzido.
6. **Número Derivado do Fundamento**: Tolerância de reprodução numérica rigorosa (ex: $|\Delta| \le 0.05$) e parâmetros de amostragem/latência.

## 2. Modos de Falha Operacionais
1. **Submeter URL Genérica sem DOI Permanente**: Inserir links para posts de blog ou repositórios efêmeros em vez do identificador persistente de publicação revisada por pares (DOI).
2. **Afirmar "Reprodução Idêntica" sem Declarar a Variação $\Delta$**: Declarar que o modelo atingiu "o mesmo resultado" sem calcular o desvio numérico e a tolerância aceitável decorrente de variações estocásticas de inicialização ou otimização.

## 3. O que a Próxima Sala Assume
A sala final do curso ([`nt-mago-supremo`](file:///Users/epedro/eCodes/edevs/edge-mage/content/tracks/10-neurotech/rooms/39-nt-mago-supremo/room.yaml)) assume que você dominou a literatura canônica, concluiu a dissertação metodológica e possui todas as evidências para invocar o ritual de consagração de Mago Supremo pela rota neural.
