# História — O Teste da Reprodutibilidade

No seminário de revisão bibliográfica do programa de mestrado, um estudante apresentava sua replicação do clássico artigo de Alexandre Barachant sobre classificação riemanniana de matrizes de covariância em EEG. O artigo original reportava uma taxa média de acerto de setenta e cinco por cento em sujeitos do BCI Competition IV.

"Baixei o código de um repositório qualquer na internet e obtive noventa e oito por cento de acurácia," anunciou o estudante com um sorriso confiante. "Consegui superar os autores originais em mais de vinte pontos percentuais."

A coordenadora acadêmica olhou para a tela e balançou a cabeça negativamente.

"Quando um algoritmo publicado há dez anos por pioneiros mundiais é subitamente 'superado' por vinte pontos em uma tarde por um código de internet, noventa e nove por cento das vezes você não descobriu um novo algoritmo; você cometeu vazamento de dados entre os blocos de teste ou usou épocas sobrepostas," explicou ela com firmeza.

Ela abriu o DOI oficial 10.1109/TBME.2011.2172210 no projetor e orientou o estudante a reescrever o pipeline do zero: recalcular as matrizes de covariância com regularização, usar a distância geodésica Riemanniana na variedade diferenciável das matrizes simétricas positivas definidas e avaliar o conjunto de teste preservando rigorosamente a partição original dos autores.

Ao rodar a rotina reproduzida e auditada, o terminal registrou exatamente setenta e três por cento de acurácia — uma variação delta de apenas menos zero vírgula zero dois em relação aos setenta e cinco por cento reportados no artigo original.

"Dentro da tolerância estocástica de cinco por cento," confirmou a professora. "Agora você não tem uma ilusão inflada por bugs; você tem uma reprodução científica legítima e auditável. Registre o artefato `study-log/artifacts/neuro-paper-module-msc.md` com o DOI e sua análise crítica. Você agora pensa e pesquisa como um mestre."
