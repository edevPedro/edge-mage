# Conceito — Arquitetura de Loop Online e Janelas Deslizantes

O teste em loop online simulado (Online Stub) é o estágio de verificação de integração que emula o comportamento exato de uma sessão de BCI em tempo real sem depender de hardware físico ou voluntários humanos.

## 1. A Dinâmica do Janelamento Deslizante (Sliding Window)
Em tempo real, as predições de intenção do usuário são geradas a uma taxa periódica fixa determinada pelo passo da janela (step ou hop size):
- **Comprimento da Janela ($W$):** Define a quantidade de histórico temporal utilizada para computar a potência de banda ou covariância (ex. $100\text{--}500\text{ ms}$).
- **Passo / Deslocamento ($S$):** Define o intervalo entre sucessivas inferências (ex. $100\text{ ms} = 10\text{ predições por segundo}$).

Para uma série temporal contínua com $T$ amostras, as coordenadas de início de cada janela são geradas pela progressão aritmética:
$$\text{início}_k = k \times S, \quad \text{fim}_k = \text{início}_k + W$$
Para todos os índices onde $\text{fim}_k \le T$.

## 2. A Estrutura do Loop de Tempo Real
O ciclo de execução contínua compreende:
```text
Ingestão de Amostras (Stream) 
   → Atualização do Buffer Circular 
   → Gatilho de Temporização (Step expirou)
   → Extração da Janela Atual [T - W : T]
   → Pré-Processamento Causal + Inferência
   → Geração do Rótulo (Label) e Comando
   → Registro em Log (Timestamp, Predição, Latência)
```

## 3. Modos de Falha na Prática de Engenharia
1. **Deriva Temporal do Loop (Clock Drift):** Usar `time.sleep()` fixo no loop em vez de sincronização baseada no número acumulado de amostras ingeridas, acumulando atraso em relação ao relógio de amostragem de hardware.
2. **Índices de Janela Fora dos Limites:** Tentar acessar janelas maiores do que as amostras disponíveis no buffer circular durante os primeiros segundos de inicialização do sistema (cold start).

## 4. O que a Próxima Sala Assume
A próxima sala (`nt-checkpoint-paper`) formaliza a consolidação do percurso através de um módulo de reprodução e análise crítica de artigo científico seminal de BCI.

## 5. Ponto de Destrave do Lab
Para o estudo de arquiteturas de BCI online em código aberto, consulte a documentação e código do [BCILAB (Swartz Center for Computational Neuroscience)](https://sccn.ucsd.edu/wiki/BCILAB) e [OpenViBE Online Scenarios](http://openvibe.inria.fr/).
