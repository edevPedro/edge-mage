# História — A Ficha de Rejeição do Revisor 2

Na sala de reuniões do grupo de pós-graduação em neuroengenharia, uma pesquisadora lia consternada o parecer emitido por um periódico internacional sobre o manuscrito de sua dissertação de mestrado. O parecer do Revisor 2 continha uma única recomendação categórica: rejeição imediata sem direito a nova submissão.

"A metodologia descrita é um buraco negro estatístico," dizia o texto do revisor. "O autor afirma ter alcançado noventa e dois por cento de acurácia, mas não informa a semente de números aleatórios, utiliza normalização z-score antes da validação cruzada, omite a ordem e a causalidade dos filtros digitais e não declara os critérios de exclusão de artefatos biológicos."

O orientador do laboratório puxou uma cadeira e sentou-se ao lado dela.

"A ciência não aceita confiança cega nem mágica de caixa preta," explicou ele. "A seção de Métodos é o contrato de integridade de um pesquisador. Se outro laboratório em Tóquio ou Berlim baixar os dados abertos do BCI Competition IV, rodar seu código com a mesma semente quarenta e dois e aplicar os mesmos biquads causais de dez hertz, eles têm a obrigação matemática de chegar no mesmo Kappa de Cohen de zero vírgula sessenta e cinco."

A mestranda pegou o modelo formal do repositório e começou a reconstruir o artefato `study-log/artifacts/neuro-thesis-methods.md`. Ela detalhou cada componente: os vinte e dois canais a duzentos e cinquenta hertz, o particionamento em blocos sem vazamento temporal, o threshold de cem microvolts para descarte de piscadas oculares, a regularização de Ledoit-Wolf no classificador linear e a latência determinística de quarenta milissegundos.

Ao submeter o memorial reestruturado ao harness de verificação, o validador automatizado conferiu cada exigência de reprodutibilidade, emitindo o carimbo de conformidade metodológica. A pesquisa agora estava blindada contra qualquer contestação.
