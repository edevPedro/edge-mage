# História — O Eixo Dominante do Córtex Motor

Na bancada de calibração de um receptor portátil de EEG, dois canais ($C3$ e $C4$) monitoram voluntários realizando tarefas de imagética motora. O algoritmo de redução de dimensionalidade precisa projetar os sinais em tempo real sobre o eixo de maior variância antes de alimentar a rede neural embarcada no microcontrolador.

O microcontrolador Cortex-M não possui memória suficiente para linkar bibliotecas completas de álgebra linear numérica como LAPACK. O desenvolvedor decide implementar um algoritmo leve: o método das potências (power iteration). Ele precisa extrair o autovetor dominante de uma matriz de covariância $2 \times 2$ calculada a partir de uma janela de sincronização motora.

No primeiro teste com a matriz $\Sigma = \begin{bmatrix} 4.0 & 0.0 \\ 0.0 & 1.0 \end{bmatrix}$, o desenvolvedor itera sem normalizar o vetor a cada passo. Em poucas multiplicações, os números estouram a representação de ponto flutuante de precisão simples. O engenheiro de firmware intervém: a cada passo de multiplicação matriz-vetor, o resultado deve ser rigorosamente dividido por sua norma euclidiana $\|Av\|_2$.

Aplicando a normalização iterativa e o quociente de Rayleigh $\lambda = v^T \Sigma v$, a rotina isola instantaneamente o autovalor dominante de $4.0\ \mu\text{V}^2$ no canal $C3$, fornecendo ao classificador o filtro espacial ótimo sem sobrecarregar a CPU embarcada.
