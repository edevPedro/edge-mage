# História — A Dança da Co-Adaptação

Era a terceira semana de testes clínicos de um decodificador de prótese robótica guiada por eletroencefalografia. O modelo preditivo havia sido treinado na segunda-feira da primeira semana com acurácia de 92%. Mas, na manhã de quarta-feira, a acurácia despencou para 68%.

O cientista de dados olhava incrédulo para os logs:

— "O código de inferência não foi alterado. O filtro passa-faixa é o mesmo. Os hiperparâmetros do LDA estão congelados. Como um modelo matemático determinístico pode perder 24 pontos percentuais de acurácia de uma semana para outra?"

O neurocientista do grupo conectou o monitor de espectro:

— "Seu modelo assume a hipótese estatística mais confortável e mais perigosa de machine learning: que os dados são independentes e identicamente distribuídos (i.i.d.). Mas você não está classificando imagens estáticas de gatos e cachorros; você está acoplado a um cérebro vivo."

Ele apontou para a distribuição de potência em torno de 12 Hz:

— "Veja o ritmo sensoriomotor do participante. Na primeira semana, ele precisava se esforçar conscientemente imaginando o fechamento do punho para modular o ritmo mu. Ao longo de duas semanas usando o dispositivo, os circuitos corticais dele passaram por neuroplasticidade hebbiana: sinapses foram fortalecidas, outras podadas, e o padrão de ativação neural mudou para otimizar o controle com menos esforço metabólico. O usuário se adaptou ao decodificador. Mas o decodificador permaneceu congelado."

O cientista de dados compreendeu o dilema:

— "Então o BCI é um sistema de malha fechada com dois agentes que aprendem simultaneamente?"

— "Exatamente", confirmou o pesquisador. "É o fenômeno da co-adaptação. Se o decodificador não permitir calibrações de rotina entre sessões diárias, ou se recalibrar agressivamente demais a ponto de perseguir uma meta móvel, o sistema diverge. Compreender a regra sináptica de Hebb é o primeiro passo para não culpar o usuário pelo fracasso da hipótese i.i.d."
