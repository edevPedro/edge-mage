# Conceito — Complexidade Computacional e Orçamento de Tempo Real em BCI

## 1. O Trade-Off Fundamental: Resolução Espacial vs. Custo Computacional
Em interfaces cérebro-computador multicanal, o número de canais $C$ e o tamanho da janela temporal $W$ (em amostras) determinam a carga algorítmica:

| Operação | Complexidade Temporal | Impacto em Tempo Real |
| :--- | :--- | :--- |
| Filtragem Temporal IIR | $\mathcal{O}(C)$ por amostra | Muito leve; linear no número de canais |
| Filtragem Temporal FIR | $\mathcal{O}(C \cdot L)$ ($L = \text{taps}$) | Moderado; paralelizado via SIMD |
| Covariância Espacial ($X X^T$) | $\mathcal{O}(C^2 W)$ por bloco | Quadrático em $C$; crítico em alta densidade |
| Inversão de Matriz / CSP / LDA | $\mathcal{O}(C^3)$ | Cúbico em $C$; proibitivo calcular a cada amostra |

Reduzir o número de canais $C$ selecionando subconjuntos anatômicos (ex: apenas $C3, Cz, C4$ para imagética motora) reduz o custo de covariância com o quadrado da redução: passar de 64 para 8 canais reduz a complexidade da covariância por um fator de $(64/8)^2 = 64\times$.

## 2. O Orçamento de Latência (Latency Budget)
Em um sistema de malha fechada, cada amostra ou bloco de amostras possui um prazo estrito (*deadline*) para ser adquirido, filtrado, decodificado e transformado em ação motora ou estimulação:

$$T_{total} = T_{acq} + T_{filter} + T_{feature} + T_{decode} + T_{actuation} \le T_{deadline}$$

Se a taxa de amostragem é $f_s = 1000\text{ Hz}$, uma nova amostra chega a cada $1000\ \mu\text{s}$. Se o algoritmo demorar $1500\ \mu\text{s}$ para processar cada amostra, o buffer de entrada acumula atraso continuamente até o esgotamento de memória (*buffer overflow*).

## 3. Modo de Falha Típico: Jitter Cumulativo e Queda de Pacotes
Quando o tempo de processamento por amostra excede o período de amostragem, o sistema entra em colapso temporal:
- A latência ponta-a-ponta cresce linearmente com o tempo de sessão.
- O feedback ao usuário dessincroniza do estado cognitivo atual.
- A thread de aquisição é bloqueada ou descarta pacotes no driver.

## 4. O Que a Próxima Sala Assume
A próxima sala (`nt-cs-ringbuf-ds`) implementa a estrutura de dados canônica para desacoplar a taxa de aquisição da taxa de consumo: o buffer circular (*ring buffer*).
