# História — A Formulação da Pergunta Científica

Na sala de reuniões de um programa de pós-graduação em neuroengenharia, um estudante senta-se diante de sua orientadora com uma proposta inicial de dissertação de mestrado. O documento traz um título genérico: "Uso de Inteligência Artificial Avançada para Decodificar Ondas Cerebrais".

A orientadora coloca o rascunho de lado com um sorriso paciente:
— Este não é um projeto de pesquisa científica; é uma declaração de intenções tecnológicas vagas — explica a orientadora. — A ciência não avança com perguntas abertas como "o que acontece se jogarmos um modelo gigante em cima de dados de EEG". Uma proposta de mestrado rigorosa requer uma **pergunta científica precisa**, uma **hipótese nula testável**, uma **métrica quantitativa de desfecho** e um **protocolo metodológico estrito**.

Ela orienta o estudante a estruturar a proposta em cinco seções fundamentais:
1. **Pergunta de Pesquisa:** "A regularização de covariância por contração de Ledoit-Wolf melhora significativamente a estabilidade do decodificador CSP+LDA em conjuntos de calibração ultra-curtos ($N \le 20$ ensaios) em comparação à matriz empírica?"
2. **Dataset e Amostra:** PhysioNet EEG Motor Movement/Imagery Dataset (109 sujeitos, 64 canais, protocolo aberto de acesso público).
3. **Métrica Primária:** Coeficiente Kappa de Cohen ($\kappa$) avaliado por validação cruzada 5-fold aninhada em blocos de ensaios completos.
4. **Governança Ética:** Pesquisa exclusivamente educacional/não-clínica sobre dados desidentificados de repositório público com termo de uso compatível.
5. **Cronograma Realista:** Três meses de benchmarking offline, dois meses de validação em firmware de tempo real e um mês para redação da dissertação.

— Quando sua pergunta é cirúrgica, o experimento pode ser executado, os resultados podem ser auditados e a resposta contribui com um tijolo real para o conhecimento da comunidade — conclui a orientadora.

O estudante reescreve a proposta em formato estruturado no diretório de artefatos (`study-log/artifacts/research-proposal.md`). O projeto é aprovado pelo colegiado acadêmico, autorizando o início formal do desenvolvimento da pesquisa.
