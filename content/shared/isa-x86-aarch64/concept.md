**Same IR idea, two ABIs.** SysV x86_64 ≈ early args in `rdi`/`rsi`/…, int return `rax`.  
AAPCS64 ≈ early args `x0`–`x7`, int return `w0`/`x0`. Godbolt two targets beats memorizing mnemonics.
