# História — A Armadilha da Sequência Repetida

Em um experimento de calibração de BCI motora, um pesquisador desenhou o protocolo de estimulação visual apresentando primeiro 20 ensaios consecutivos da mão direita e, em seguida, 20 ensaios consecutivos da mão esquerda. Ao treinar um classificador linear, a acurácia no conjunto de teste atingiu impressionantes 91%.

No dia seguinte, ao tentar utilizar o mesmo modelo decodificador com classes sorteadas aleatoriamente, a acurácia desmoronou para 48%.

O coordenador do laboratório abriu os traçados temporais e apontou o erro clássico de desenho experimental:
— Em EEG, a impedância dos eletrodos sofre deriva eletroquímica contínua ao longo do tempo (drift de baseline), a fadiga cognitiva aumenta e a temperatura da sala varia — explica o coordenador. — Quando você coloca 20 ensaios da mesma classe em bloco contínuo, a média do sinal no início do experimento é completamente diferente da média no final do experimento devido à deriva física, e não à imagética. O classificador não aprendeu a intenção motora: aprendeu o horário em que o ensaio ocorreu!

Ele detalhou as regras fundamentais do desenho de ensaios (Trial Design):
1. **Pseudoaleatorização com Balanceamento em Blocos:** As classes devem ser sorteadas aleatoriamente dentro de pequenos blocos balanceados (por exemplo, blocos de 4 ensaios contendo exatamente 2 de cada classe em ordem sorteada).
2. **Controle de Sequência Máxima (Max Streak):** Nenhuma classe pode se repetir mais do que três vezes consecutivas, evitando que o voluntário antecipe o próximo estímulo ou entre em modo automático.
3. **Intervalo Inter-Ensaios Variável (Jittered ITI):** O tempo de repouso entre ensaios deve variar aleatoriamente entre 1.5 e 2.5 segundos para impedir que o ritmo do relógio seja antecipado pelo córtex visual (potencial de prontidão de Bereitschaftspotential).

O pesquisador implementa a função `max_streak` para auditar a sequência de marcadores de evento. O novo protocolo de calibração elimina os vieses de deriva e garante que o classificador aprenda exclusivamente padrões neurais genuínos.
