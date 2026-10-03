# Conceito — Organização Cortical, Homúnculo de Penfield e Sistema 10–20

## 1. Topografia Funcional e Organização Contralateral
O cérebro humano exibe uma organização somatotópica rígida no córtex cerebral:
- **Área Motora Primária (M1 - Área 4 de Brodmann):** Localizada no giro pré-central, emite os comandos motores via trato corticoespinhal.
- **Área Somatossensorial Primária (S1 - Áreas 3, 1, 2 de Brodmann):** Localizada no giro pós-central, processa aferências táteis e proprioceptivas.
- **Decussação das Pirâmides:** A via corticoespinhal cruza o bulbo em direção à medula contralateral. Consequentemente:
  - Intenção e imagética motora da **mão direita** provocam modulação neural (ERD/ERS) primariamente no **hemisfério cerebral esquerdo**.
  - Intenção da **mão esquerda** modula o **hemisfério cerebral direito**.
  - Movimentos de membros inferiores (pés) concentram-se na face medial dos hemisférios, projetando-se próximo à linha média sagital ($Cz$).

## 2. O Sistema Internacional 10–20 de Eletrodos
Padronizado por Herbert Jasper em 1958 para a Federação Internacional de Sociedades de EEG, o sistema posiciona eletrodos com base em porcentagens (10% e 20%) das distâncias cranianas relativas (Násion-Ínion e Pré-auricular Esquerdo-Direito):

### Nomenclatura das Regiões Corticais:
- **Fp:** Frontopolar
- **F:** Frontal
- **C:** Central (sulco central / áreas motoras e sensoriais)
- **T:** Temporal
- **P:** Parietal
- **O:** Occipital

### Regras de Hemisfério e Linha Média:
- **Índices Ímpares (1, 3, 5, 7):** Posicionados sobre o **hemisfério esquerdo** (ex: $C3, F3, P3, O1$).
- **Índices Pares (2, 4, 6, 8):** Posicionados sobre o **hemisfério direito** (ex: $C4, F4, P4, O2$).
- **Sufixo 'z' ou 'Z' (Zero):** Posicionados estritamente sobre a **linha média** ou vértex craniano (ex: $Fz, Cz, Pz, Oz$).

## 3. Limites de Interpretação e Não-Diagnóstico
A atribuição anatômica de sinais de EEG de superfície é limitada pela condução de volume do crânio. Dizer que um sinal em $C3$ vem exclusivamente de M1 é uma aproximação de engenharia; o eletrodo capta um somatório ponderado de áreas motoras, pré-motoras e sensoriais adjacentes. Nenhum pipeline de BCI experimental substitui imagens de ressonância magnética funcional (fMRI) ou diagnósticos clínicos neurológicos.

## 4. O Que a Próxima Sala Assume
A próxima sala (`nt-neuro-plasticity`) estuda a neuroplasticidade sináptica e a co-adaptação bidirecional entre o usuário humano e os pesos estatísticos do decodificador.
