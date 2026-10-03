# História — O epoch que não era a sessão inteira

No laboratório de imagética, o synth deixa na mesa um vetor de amostras `0…99` — índice, não microvolt de sujeito. O cue cai na amostra 50. A aprendiz puxa a sessão inteira; o guardião marca pre=5 e post=10 e exige `slice_epoch` naquele trigger.

O recorte é o meio-aberto `[50−5, 50+10) = [45, 60)`. No vetor, o primeiro valor é 45, o último é 59 e o comprimento é 15. Quarenta amostras seria outro par pre/post; cem seria a sessão. Sem esse corte, a potência mistura baseline com MI.

No quadro ele escreve 45, 46, …, 59 e conta quinze posições. Se pre=10 e post=30, o comprimento vira 40 e o primeiro índice deixa de ser 45 — a Sala recusa. Unidade: amostra, não ms. C3 segue contralateral à mão direita; ERD é queda de mu/beta, e o synth não é fisiologia.

Fase F7, sala nt-mi-paradigm: a task de código chama-se slice_epoch. Entregar a sessão ou a janela de bandpower de 2 s no lugar do epoch quebra o contraste esquerda/direita antes mesmo do filtro.
