# Bits & two's complement (shared)

Computers store integers as **bits**. A **byte** is 8 bits. Hex is a compact view of bit groups.

**Two's complement** makes subtraction into addition: negate by invert-bits then +1. In *n*-bit two's complement, the all-ones pattern is always **-1**.

Overflow is modular wrap on the word size — not a mystery once you fix the bit width. LLVM IR integer types (`i8`, `i32`, …) are bit-width first; signedness is in the *operations* ([LangRef — Integer Type](https://llvm.org/docs/LangRef.html#integer-type)).

`room_id: bits` — one credit across Systems and Edge maps. Pair with [CSAPP student materials](https://csapp.cs.cmu.edu/3e/students.html) / Data Lab ideas when you advance.
