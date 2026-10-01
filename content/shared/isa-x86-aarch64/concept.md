**Glance only.** SysV x86_64 ≈ early args `rdi`/`rsi`/…, int return `rax`.  
AAPCS64 ≈ early args `x0`–`x7`, int return `w0`/`x0`.  
**Why edge ≠ desktop:** power/area/thermal — not “learn both ISAs cold.” Godbolt two targets beats mnemonic farm.
