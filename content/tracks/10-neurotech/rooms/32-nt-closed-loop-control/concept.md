# Conceito — BCI como Sistema de Controle em Malha Fechada e Suavização Exponencial

Uma Interface Cérebro-Computador em tempo real forma uma malha fechada de bio-feedback: a intenção do usuário gera biopotenciais, o decodificador atua sobre o ambiente, e o usuário observa o efeito sensorial para corrigir a trajetória mental.

## 1. A Malha Fechada de Controle (Closed-Loop BCI)
O diagrama de blocos canônico compreende:
```text
Cérebro (Controlador) 
   → Biopotencial (EEG) 
   → Decodificador (Planta com Atraso t_decide) 
   → Atuador (Cursor/Robô com Atraso t_act) 
   → Feedback Visual/Sensorial (Atraso t_visual ≈ 150 ms) 
   → Cérebro (Correção de Erro)
```

### Atraso de Transporte e Instabilidade Dinâmica
Pela teoria clássica de controle de Nyquist e Bode, a presença de atraso de transporte puro ($e^{-s T}$) introduz uma queda de fase linear com a frequência. Se o ganho da interface for excessivamente alto ou as predições variarem abruptamente, a margem de fase torna-se negativa, gerando instabilidade oscilatória divergente.

## 2. Suavização Exponencial (Exponential Moving Average - EMA)
Para amortecer transientes espúrios e estabilizar comandos contínuos de direção ou velocidade:
$$y[t] = \alpha \cdot x[t] + (1 - \alpha) \cdot y[t-1]$$
Onde $\alpha \in (0, 1]$ é o fator de suavização:
- $\alpha \to 1$: Resposta instantânea, mas suscetível a ruído e solavancos.
- $\alpha \to 0$: Alta estabilidade e filtragem de ruído, mas introduz inércia temporal perceptível.
- Valores típicos em BCI: $\alpha = 0.15\text{--}0.30$.

## 3. Modos de Falha na Prática de Engenharia
1. **Ganho Excessivo no Feedback:** Mover o cursor com velocidade excessiva, fazendo o voluntário ultrapassar o alvo repetidamente (overshoot).
2. **Ignorar Latência Sensorial:** Assumir que o usuário pode reagir a um erro de classificação antes de 150 milissegundos.

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-irb-protocol`) formaliza os procedimentos regulatórios de Comitê de Ética em Pesquisa (IRB) para estudos com voluntários humanos.

## 5. Ponto de Destrave do Lab
Para o estudo da modelagem de BCI sob a teoria de controle em malha fechada, consulte [Müller-Putz et al. (Front Neurosci 2015, Closed-loop BCI)](https://doi.org/10.3389/fnins.2015.00078) e [Shanechi (Nat Commun 2019, Brain-machine interfaces from motor to mood)](https://doi.org/10.1038/s41467-019-12497-z).
