# História — Deadline de 40 ms

O loop pede feedback. Sense engole 128 ms só para encher a janela.
O deadline de 40 ms estoura — e isso **ensina**, não é bug escondido.

MI real costuma tolerar latências maiores; 40 ms é stress case de hard-RT.
