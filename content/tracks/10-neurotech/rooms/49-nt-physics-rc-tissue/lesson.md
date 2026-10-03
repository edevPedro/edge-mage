# Lição — Tecido como Circuito RC

## 1. O Circuito Equivalente de Membrana
A membrana celular em repouso e durante a condução passiva (eletrotônica) é descrita pela equação de cabo e pelo circuito RC equivalente:
1. **Resistência de Membrana ($R_m$)**: Representa a condutância dos canais iônicos de repouso ($K^+$ de vazamento).
2. **Capacitância de Membrana ($C_m$)**: Representa o acúmulo de cargas iônicas através da bicamada lipídica isolante.
3. **Constante de Tempo ($\tau_m = R_m C_m$)**:
   $$\tau_m = R_m C_m \implies f_c = \frac{1}{2\pi \tau_m}$$

## 2. A Resposta em Frequência $|H(f)|$
Em termos de teoria linear de sistemas, a membrana responde a sinais oscilatórios com função de transferência de passa-baixa de primeira ordem:
$$|H(f)| = \frac{1}{\sqrt{1 + (2\pi f R C)^2}}$$
- Sinais biológicos de baixa frequência (como oscilações $\theta$, $\alpha$ e $\beta$ entre $4$ e $30\text{ Hz}$) operam próximos da frequência de corte ou na banda de passagem, atravessando com perda moderada ($<3\text{ dB}$).
- Flutuações ultra-rápidas (componentes de borda de subida de spikes axônicos em $1\text{ kHz}$) encontram impedância capacitiva residual $1/(2\pi f C)$ desprezível, sofrendo derivação (*shunting*) e atenuação drástica ($>30\text{ dB}$).

## 3. Funções no Laboratório
- `rc_cutoff(r_ohms, c_farads)`: Calcula a frequência de corte de 3 dB em Hz.
- `audit_tissue_filtering(f_hz, r_membrane_ohm, c_membrane_farad)`: Avalia quantitativamente a resposta em amplitude $|H(f)|$ e atenuação em dB, verificando se a frequência de teste está contida na banda passante biológica ($\ge -3.0\text{ dB}$).

Para destravar o lab, abra [Einevoll et al. LFP review (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3884846/) e leia o modelo de tecido e campo extracelular em Einevoll para a constante de tempo do RC não virar um filtro decorativo.
