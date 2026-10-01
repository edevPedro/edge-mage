# Systems boss craft

**Mago Supremo gate (Systems axis).** Completing FLAG rooms alone is not enough — you must leave a verifiable compilers/systems artifact.

## Outside the grimório (definition of done)

1. **Emit IR:** `clang -emit-llvm -S toy.c -o toy.ll` (or equivalent). Keep the `.ll` in the study log or a linked repo.
2. **Transform:** run `opt -S -passes='default<O2>' toy.ll -o toy.opt.ll` **or** a tiny New PM pass (`OptionalPassInfoMixin` + `PassBuilder` / `-load-pass-plugin`) per [Writing an LLVM Pass (New PM)](https://llvm.org/docs/WritingAnLLVMNewPMPass.html) and [Using the New Pass Manager](https://llvm.org/docs/NewPassManager.html).
3. **Diff:** paste a short before/after IR snippet (3–20 lines) showing what changed (DCE, simplify, your pass print, etc.).
4. **LangRef cite:** open [LangRef](https://llvm.org/docs/LangRef.html) and name one type or instruction you actually used (e.g. `i32`, `getelementptr`, `ret`).
5. **ABI / object literacy (pick one):**
   - SysV: cite [x86-64 psABI](https://gitlab.com/x86-psABIs/x86-64-ABI) for one arg/return register you saw in asm, **or**
   - AAPCS64: cite [aapcs64.rst](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst) for `x0`/`w0` (or FP `d0`), **or**
   - ELF: `readelf -S` / `llvm-objdump -d` note on `.text` ([man elf](https://man7.org/linux/man-pages/man5/elf.5.html), [llvm-objdump](https://llvm.org/docs/CommandGuide/llvm-objdump.html)).
6. Write `study-log/artifacts/systems-boss-craft.md` with the fields below, then seal the ritual in-app.

### Required fields in `systems-boss-craft.md`

```markdown
## Pipeline
commands: …

## IR diff
\`\`\`
before…
after…
\`\`\`

## LangRef
cite: … (URL + name)

## ABI or ELF
cite: … (psABI / AAPCS64 / elf + what you observed)

## Notes
(optional)
```

Optional RE flavor: a one-paragraph lift note (objdump / Capstone) under `## Notes` — still not a substitute for IR + LangRef + ABI/ELF.

## Official anchors (do not invent flags)

- https://llvm.org/docs/LangRef.html
- https://llvm.org/docs/CommandGuide/opt.html
- https://llvm.org/docs/CommandGuide/llc.html
- https://llvm.org/docs/WritingAnLLVMNewPMPass.html
- https://llvm.org/docs/NewPassManager.html
- https://gitlab.com/x86-psABIs/x86-64-ABI
- https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst
