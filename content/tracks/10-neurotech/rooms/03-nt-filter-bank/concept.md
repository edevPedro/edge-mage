# Conceito — Banco de filtros

Um **filter bank** aplica vários passa-banda (ex. mu 8–12 Hz, beta 16–24 Hz) e extrai energia/potência por canal (ou covariâncias por banda).

- Escolha de banda = hipótese fisiológica + o que o ADC/fs permitem.
- Notch 50/60 Hz trata artefato de linha — não é “feature neural”.
- Anti-aliasing e `fs` vêm da cadeia elétrica (Nyquist).

Animação alvo: `filter_freq_response` — ver o ganho na banda útil cair fora dela.
