# História — A Respiração dos Ritmos Sensoriomotores

No centro de pesquisas em neuroreabilitação motora, um monitor exibia os espectrogramas em tempo real de um voluntário que realizava um experimento com interface cérebro-computador. O protocolo era rigorosamente cronometrado: quatro segundos de repouso olhando para uma cruz no centro da tela, seguidos por quatro segundos de imagética motora contínua abrindo e fechando a mão direita imaginária.

O desenvolvedor responsável pelo pipeline de DSP olhava para a potência espectral nos canais C3 e C4:

— "Durante o repouso, a potência em 10 Hz no canal C3 é enorme: quase 40 microvolts ao quadrado. Mas, assim que surge a instrução de imagética motora, a potência cai para menos de 10 microvolts ao quadrado. O sinal quase desapareceu! Temos um problema de atenuação na aquisição?"

O neuroengenheiro líder riu alto e apontou para o traçado:

— "Não é problema de hardware; é a assinatura biofísica mais pura do córtex motor primário. Você está testemunhando a Dessincronização Relacionada a Eventos — o clássico ERD descoberto por Gert Pfurtscheller."

O neuroengenheiro desenhou os blocos no quadro:

— "Quando a área sensoriomotora está em repouso, milhões de neurônios piramidais disparam em fase e em sincronia, sustentados por alças talamocorticais rítmicas. Essa sincronia maciça produz ondas de alta voltagem em 10 Hz — o ritmo mu. Quando o voluntário engaja em planejamento ou execução motora, as redes corticais se desincronizam para processar informação em paralelo. Cada neurônio dispara em seu próprio tempo. A potência macroscópica medida no escalpo desaba."

Ele voltou-se para o desenvolvedor:

— "Depois que o movimento cessa, a potência salta subitamente para um patamar até superior ao repouso inicial — a Sincronização Relacionada a Eventos (ERS), ou rebote beta. Para extrair essa métrica em tempo real, calculamos a variação percentual de potência relativa à linha de base. Um valor positivo indica dessincronização funcional (ERD); um valor negativo indica sincronização de rebote (ERS). Implemente esse cálculo com rigor numérico, pois ele alimentará todo o seu classificador de LDA."
