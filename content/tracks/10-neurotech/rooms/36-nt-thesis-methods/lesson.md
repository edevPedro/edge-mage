# Lição — Módulo Methods: Reprodutibilidade e Blindagem Científica

## 1. O Padrão Methods em Neurotecnologia
A redação metodológica deve responder sem ambiguidade:
1. **Aquisição**: Taxa de amostragem ($f_s$), topografia de eletrodos (10-20), impedância máxima permitida ($<5\text{ k}\Omega$).
2. **Pré-Processamento Causal**: Tipologia e ordem dos filtros digitais, frequências de corte de -3 dB, estado dos registradores de atraso.
3. **Validação Cruzada**: Divisão contígua em blocos (`split_blocked`) para impedir vazamento temporal.
4. **Hiperparâmetros e Sementes**: Parâmetros de shrinkage ($\gamma$), número de componentes espaciais e fixação de sementes (`seed=42`).

## 2. A Função de Laboratório
- `validate_methods_checklist(spec)`: Avalia uma especificação de Methods contra violações epistemológicas (filtros acausais em loops causais, splits aleatórios com vazamento, ausência de parâmetros de reprodutibilidade).

Para destravar o lab, abra [MNE-Python documentation](https://mne.tools/stable/index.html) e leia a cadeia reprodutível do MNE (pré-processamento explícito, não só o κ final) para o checklist de Methods ter filtro, feature e split.
