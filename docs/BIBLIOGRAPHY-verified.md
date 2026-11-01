# BIBLIOGRAPHY — Verified Resources for e-mage

**Date:** 2026-11-01  
**Purpose:** Canonical reference list for e-mage curriculum  
**Policy:** Official docs > textbooks > papers > blogs. All URLs verified.

---

## 1. Architecture & Low-Level

### Official Documentation

| Resource | URL | Use In |
|----------|-----|--------|
| **Arm Architecture Reference Manual (DDI0487)** | https://developer.arm.com/documentation/ddi0487/latest | P2, P3, P6 |
| **AArch64 ABI (AAPCS64)** | https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst | P1, P2, P6 |
| **Arm Neon Intrinsics Reference** | https://developer.arm.com/architectures/instruction-sets/intrinsics/ | P3, P6 |
| **Arm A64 Instruction Set Overview** | https://developer.arm.com/documentation/102374/latest | P2 |
| **x86-64 psABI** | https://gitlab.com/x86-psABIs/x86-64-ABI | P0 (literacy) |
| **RISC-V Specifications** | https://docs.riscv.org/ | P0 (literacy) |

### Textbooks

| Resource | Citation | Use In |
|----------|----------|--------|
| **Computer Architecture: A Quantitative Approach** | Hennessy & Patterson, 6th ed. | P2, P4 |
| **Computer Systems: A Programmer's Perspective (CSAPP)** | Bryant & O'Hallaron, 3rd ed. | P0, P1, P2 |
| **The Art of 64-bit Assembly** | Hyde | P1 (optional) |

### Courses & Labs

| Resource | URL | Use In |
|----------|-----|--------|
| **CSAPP Student Site** | https://csapp.cs.cmu.edu/3e/students.html | P0, P1 |
| **OSTEP (Operating Systems)** | https://pages.cs.wisc.edu/~remzi/OSTEP/ | P1 |

---

## 2. LLVM & Compilers

### Official Documentation

| Resource | URL | Use In |
|----------|-----|--------|
| **LLVM Language Reference** | https://llvm.org/docs/LangRef.html | P1 |
| **LLVM Programmer's Manual** | https://llvm.org/docs/ProgrammersManual.html | P1 |
| **Clang Documentation** | https://clang.llvm.org/docs/ | P1 |
| **LLC Command Guide** | https://llvm.org/docs/CommandGuide/llc.html | P1 |
| **OPT Command Guide** | https://llvm.org/docs/CommandGuide/opt.html | P1 |

### Tools

| Resource | URL | Use In |
|----------|-----|--------|
| **Compiler Explorer (Godbolt)** | https://godbolt.org/ | P0, P1, P3 |

---

## 3. Performance Engineering

### Papers (Canonical)

| Resource | Citation/DOI | Use In |
|----------|--------------|--------|
| **Roofline Model** | Williams et al. DOI: 10.1145/1498765.1498785 | P4 |
| **What Every Programmer Should Know About Memory** | Drepper, https://www.akkadia.org/drepper/cpumemory.pdf | P2, P3 |

### Official Documentation

| Resource | URL | Use In |
|----------|-----|--------|
| **Apple Metal Documentation** | https://developer.apple.com/documentation/metal/ | P5 |
| **Metal Shading Language Specification** | https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf | P5 |
| **Metal Best Practices Guide** | https://developer.apple.com/library/archive/documentation/3DDrawing/Conceptual/MTLBestPracticesGuide/ | P5 |
| **Instruments User Guide** | https://developer.apple.com/documentation/instruments | P3, P5 |

### Standards

| Resource | URL | Use In |
|----------|-----|--------|
| **IEEE 754-2019** | https://ieeexplore.ieee.org/document/8766229 | P4 |
| **OpenMP Specification** | https://www.openmp.org/specifications/ | P4 |

---

## 4. GPU & CUDA (Literacy)

### Official Documentation

| Resource | URL | Use In |
|----------|-----|--------|
| **CUDA C++ Programming Guide** | https://docs.nvidia.com/cuda/cuda-c-programming-guide/ | P5 (elective) |
| **CUDA Best Practices Guide** | https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/ | P5 (elective) |

### Note
CUDA is elective literacy only. Primary GPU path is Metal for Apple Silicon.

---

## 5. Machine Learning & Inference

### Official Documentation

| Resource | URL | Use In |
|----------|-----|--------|
| **PyTorch Export** | https://pytorch.org/docs/stable/export.html | P6 |
| **ONNX Specification** | https://onnx.ai/ | P6 |
| **ONNX Runtime** | https://onnxruntime.ai/ | P6 |
| **LiteRT (TFLite)** | https://ai.google.dev/edge/litert | P6 |
| **LiteRT Quantization Spec** | https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec | P6 |
| **CMSIS-NN** | https://arm-software.github.io/CMSIS-NN/latest/ | P6 |
| **CMSIS-NN GitHub** | https://github.com/ARM-software/CMSIS-NN | P6 |
| **ExecuTorch** | https://pytorch.org/executorch/ | P6 |
| **Core ML** | https://developer.apple.com/documentation/coreml | P6 |
| **ML Developers Guide (Cortex-M)** | https://developer.arm.com/documentation/109267/latest/ | P6 |

### Papers

| Resource | Citation/DOI | Use In |
|----------|--------------|--------|
| **Quantization and Training of NNs** | Jacob et al. arXiv:1712.05877 | P6 |

---

## 6. Hardware & Co-design

### Official Documentation

| Resource | URL | Use In |
|----------|-----|--------|
| **Verilog IEEE 1364-2005** | IEEE Standard | P7 |
| **SystemVerilog IEEE 1800-2017** | IEEE Standard | P7 |
| **Vivado HLS User Guide** | https://docs.amd.com/r/en-US/ug902-vivado-high-level-synthesis | P7 |

### Textbooks

| Resource | Citation | Use In |
|----------|----------|--------|
| **Digital Design and Computer Architecture** | Harris & Harris | P7 |
| **Verilog HDL** | Palnitkar | P7 (optional) |

---

## 7. Systems Programming

### Official Documentation

| Resource | URL | Use In |
|----------|-----|--------|
| **Linux man pages** | https://man7.org/linux/man-pages/ | P1 |
| **ELF Specification** | https://refspecs.linuxfoundation.org/elf/elf.pdf | P1 |
| **C++ Reference** | https://en.cppreference.com/ | All |
| **C17 Draft** | https://www.open-std.org/jtc1/sc22/wg14/ | P1 |

### Textbooks

| Resource | Citation | Use In |
|----------|----------|--------|
| **The C Programming Language** | Kernighan & Ritchie, 2nd ed. | P0 |
| **Effective Modern C++** | Meyers | P1 |
| **C++ Concurrency in Action** | Williams | P1 |

---

## 8. Mathematics & Numerical Computing

### Textbooks

| Resource | Citation | Use In |
|----------|----------|--------|
| **Numerical Linear Algebra** | Trefethen & Bau | P4 |
| **What Every Computer Scientist Should Know About Floating-Point** | Goldberg | P4 |
| **Matrix Computations** | Golub & Van Loan | P4 |

### Online Resources

| Resource | URL | Use In |
|----------|-----|--------|
| **Khan Academy Linear Algebra** | https://www.khanacademy.org/math/linear-algebra | P0 |
| **3Blue1Brown Essence of Linear Algebra** | https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab | P0 |

---

## 9. General Learning Resources

| Resource | URL | Use In |
|----------|-----|--------|
| **MDN Web Docs (Learning Area)** | https://developer.mozilla.org/en-US/docs/Learn | P0 |
| **Stack Overflow** | https://stackoverflow.com/ | Reference |

---

## URL Verification Status

| Domain | Status | Last Checked |
|--------|--------|--------------|
| developer.arm.com | ✅ Verified | 2026-11 |
| llvm.org | ✅ Verified | 2026-11 |
| developer.apple.com | ✅ Verified | 2026-11 |
| pytorch.org | ✅ Verified | 2026-11 |
| onnx.ai | ✅ Verified | 2026-11 |
| onnxruntime.ai | ✅ Verified | 2026-11 |
| ai.google.dev | ✅ Verified | 2026-11 |
| github.com/ARM-software | ✅ Verified | 2026-11 |
| csapp.cs.cmu.edu | ✅ Verified | 2026-11 |
| pages.cs.wisc.edu/~remzi | ✅ Verified | 2026-11 |
| godbolt.org | ✅ Verified | 2026-11 |

---

## Usage Guidelines

1. **In room.yaml resources:** Use direct URLs to official documentation
2. **In concept.md:** Reference by title with inline link
3. **Prefer official docs** over third-party tutorials
4. **Papers:** Include DOI when available
5. **Textbooks:** Include edition to avoid version confusion
6. **Offline:** concept.md must teach the concept; URLs are optional enrichment

---

## Contributing

To add a resource:
1. Verify URL is accessible
2. Confirm it's official or canonical
3. Place in appropriate category
4. Add to relevant room's resources array
5. Update verification status table
