# SPEC — Forge: Cumulative Portfolio Project

**Product:** e-mage  
**Component:** Forge cumulative project (`content/tracks/12-emage-forge/`)  
**Status:** Full specification (2026-11-01)  
**Supersedes:** Scaffold-only Forge rooms

---

## 1. Vision

Forge is **one codebase** that evolves across the entire e-mage journey. Unlike disconnected phase bosses, Forge forces you to prove you can **transfer** the same problem through different layers of the machine: scalar reference → SIMD → Roofline analysis → GPU → inference optimization → (optional) hardware accelerator.

### What Forge Is NOT
- A collection of unrelated demos
- A "pick any project" assignment
- A benchmark-only exercise without correctness
- An excuse to skip earlier phases

### What Forge IS
- A portfolio thread showing progression
- Proof of transfer: same golden reference, different execution paths
- Evidence of measurement discipline
- A project you can show to senior engineers and use in technical interviews

---

## 2. Project Options (Choose One)

### Option A: GEMM Kernel (Recommended for HPC path)

**Matrix-matrix multiplication** is the canonical compute-bound kernel. It appears in:
- Linear algebra libraries (BLAS GEMM)
- Neural network layers (FC, Conv1x1)
- Signal processing (correlation)

**Why GEMM:**
- High arithmetic intensity makes it compute-bound on modern CPUs/GPUs
- Tiling/blocking directly impacts performance
- Natural fit for Roofline analysis
- Transfers well to Metal compute shaders
- Quantized GEMM is core of inference optimization

**Scope:** N×N matrix multiply, single precision (f32) as baseline.

### Option B: DSP Filter (Recommended for signals/edge path)

**FIR filter** or **convolution** is the canonical memory-bound kernel. It appears in:
- Audio processing
- Image filtering
- BCI signal processing (Neurotech connection)
- Neural network convolutions

**Why FIR/Conv:**
- Memory-bound at small kernel sizes
- Transitions to compute-bound with larger kernels
- Natural SIMD application (vector dot products)
- Direct connection to inference (Conv2D kernels)
- ESP32/MCU deployment realistic

**Scope:** 1D FIR filter with configurable taps, single precision.

### Option C: Physics Simulation (Recommended for HPC/scientific path)

**Heat equation / Jacobi iteration** is the canonical stencil kernel. It appears in:
- PDE solvers
- Physics simulation
- Computational fluid dynamics
- Numerical methods courses

**Why Jacobi:**
- Memory-bound stencil pattern
- Temporal blocking opportunities
- Natural parallelization
- Clear numerical stability concerns
- Good Roofline target

**Scope:** 2D heat equation, explicit Euler, single precision.

---

## 3. Stage Requirements

### F0 — Scalar Reference (P0–P1)

**Prerequisites:** Fundamentals clear, basic C/C++ toolchain

**Deliverables:**
1. **Scalar implementation** — Naive, readable, correct
2. **Test harness** — Fixed inputs, golden output, correctness check
3. **Benchmark baseline** — Wall time, N runs, machine specs
4. **Git evidence** — Clean commit history

**Pass Criteria:**
- [ ] Code compiles with `-Wall -Wextra` clean
- [ ] Tests pass with explicit tolerance (abs or rel)
- [ ] README documents: machine, compiler, flags, N, median time
- [ ] Golden output saved as reference file

**Artifact:** `study-log/artifacts/forge-f0-scalar.md`

```c
// Example structure (GEMM)
void gemm_scalar(const float* A, const float* B, float* C, int N) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            float sum = 0.0f;
            for (int k = 0; k < N; k++) {
                sum += A[i*N + k] * B[k*N + j];
            }
            C[i*N + j] = sum;
        }
    }
}
```

---

### F1 — SIMD Optimization (P3)

**Prerequisites:** P2 complete, P3 NEON rooms, Boss ARM Math

**Deliverables:**
1. **NEON implementation** — Using intrinsics or verified autovectorization
2. **Same test harness** — Golden from F0 still passes
3. **Comparison benchmark** — Scalar vs NEON, same N
4. **Vectorization evidence** — Assembly inspection or `-Rpass=vector`

**Pass Criteria:**
- [ ] NEON version produces same result as scalar (within tolerance)
- [ ] Speedup documented with measurement protocol
- [ ] Assembly shows vector instructions (provide snippet)
- [ ] Explanation of what vectorized and why

**Artifact:** `study-log/artifacts/forge-f1-simd.md`

**Key Questions to Answer:**
- What is the speedup factor?
- Which loops vectorized?
- What is the vector width actually used?
- Did data alignment help?

```c
// Example NEON (GEMM inner loop)
#include <arm_neon.h>

void gemm_neon(const float* A, const float* B, float* C, int N) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j += 4) {
            float32x4_t sum = vdupq_n_f32(0.0f);
            for (int k = 0; k < N; k++) {
                float32x4_t a = vdupq_n_f32(A[i*N + k]);
                float32x4_t b = vld1q_f32(&B[k*N + j]);
                sum = vfmaq_f32(sum, a, b);
            }
            vst1q_f32(&C[i*N + j], sum);
        }
    }
}
```

---

### F2 — Roofline Analysis (P4)

**Prerequisites:** P4 complete, Boss Physics

**Deliverables:**
1. **Arithmetic intensity calculation** — FLOPs / bytes for your kernel
2. **Peak measurements** — Measure peak FLOPS and bandwidth on your M4
3. **Roofline plot** — Place your kernel on the model
4. **Tiled implementation** — If memory-bound, implement blocking
5. **Comparison** — Before/after tiling if applicable

**Pass Criteria:**
- [ ] Arithmetic intensity documented with formula
- [ ] Peak FLOPS estimated (not invented)
- [ ] Peak bandwidth estimated (STREAM or similar)
- [ ] Kernel classified as memory-bound or compute-bound
- [ ] If tiled: improvement measured and explained

**Artifact:** `study-log/artifacts/forge-f2-roofline.md`

**Roofline Construction for M4:**
```
Peak FLOPS (f32): ~3.5 TFLOPS (estimate, varies by workload)
Peak bandwidth: ~100 GB/s (unified memory)

Arithmetic Intensity (GEMM NxN):
  FLOPs = 2*N^3
  Bytes = 3*N^2*4 (read A, B; write C)
  AI = 2*N^3 / (12*N^2) = N/6

For N=512: AI ≈ 85 flops/byte → compute-bound
For N=64:  AI ≈ 10 flops/byte → still compute-bound for GEMM
```

---

### F3 — GPU Implementation (P5)

**Prerequisites:** P5 complete, Boss Metal

**Deliverables:**
1. **Metal compute shader** — Same algorithm, GPU execution
2. **Host code** — Buffer setup, dispatch, synchronization
3. **Same golden** — GPU output matches CPU reference
4. **Performance comparison** — CPU vs GPU with transfer costs
5. **Fallback documentation** — What if GPU path not viable

**Pass Criteria:**
- [ ] Metal shader compiles and runs
- [ ] Output matches golden (with documented tolerance)
- [ ] Performance includes buffer transfer time
- [ ] Explanation of threadgroup size choice
- [ ] Honest assessment of CPU vs GPU tradeoffs

**Artifact:** `study-log/artifacts/forge-f3-metal.md`

**Metal Kernel Structure (GEMM):**
```metal
#include <metal_stdlib>
using namespace metal;

kernel void gemm(
    const device float* A [[buffer(0)]],
    const device float* B [[buffer(1)]],
    device float* C [[buffer(2)]],
    constant int& N [[buffer(3)]],
    uint2 gid [[thread_position_in_grid]])
{
    int i = gid.y;
    int j = gid.x;
    if (i >= N || j >= N) return;
    
    float sum = 0.0f;
    for (int k = 0; k < N; k++) {
        sum += A[i*N + k] * B[k*N + j];
    }
    C[i*N + j] = sum;
}
```

---

### F4 — Inference Optimization (P6)

**Prerequisites:** P6 complete, on-device ritual

**Deliverables:**
1. **Quantized version** — int8 or int16 implementation
2. **Same mathematical motif** — Not a completely different model
3. **Export evidence** — If wrapping in ONNX/CoreML
4. **Latency/RAM measurement** — On target device
5. **Accuracy analysis** — Error vs f32 golden

**Pass Criteria:**
- [ ] Quantized implementation runs
- [ ] Error vs golden documented (RMS, max abs)
- [ ] Latency measured with proper methodology
- [ ] RAM footprint documented
- [ ] Quantization strategy explained (scale, zero-point)

**Artifact:** `study-log/artifacts/forge-f4-inference.md`

**Quantization Approach:**
```c
// Affine quantization: real = (q - zp) * scale
typedef struct {
    int8_t* data;
    float scale;
    int32_t zero_point;
} QuantizedTensor;

int8_t quantize(float x, float scale, int32_t zp) {
    int32_t q = (int32_t)roundf(x / scale) + zp;
    return (int8_t)max(-128, min(127, q));
}

float dequantize(int8_t q, float scale, int32_t zp) {
    return (q - zp) * scale;
}
```

---

### F5 — Co-design (P7, Optional)

**Prerequisites:** P7 complete, Boss Accelerator

**Deliverables (choose one):**

**Option A — RTL Sketch:**
1. Verilog module for core operation (MAC, dot, etc.)
2. Testbench with same golden
3. Resource/timing estimates

**Option B — HLS Exploration:**
1. C/C++ with HLS pragmas
2. Synthesis report (II, resources)
3. Comparison vs software

**Option C — Honest Stop:**
1. Analysis of what hardware could accelerate
2. Why board/FPGA not pursued
3. Architecture proposal for future work

**Pass Criteria:**
- [ ] One of the above options completed
- [ ] Software baseline comparison
- [ ] Functional correctness demonstrated
- [ ] Limitations acknowledged

**Artifact:** `study-log/artifacts/forge-f5-codesign.md`

---

## 4. Evidence Standards

### Every Stage MUST Have:

1. **Two implementations** (baseline + optimized, or current + previous)
2. **Measurement protocol**
   - Fixed input (save test vectors)
   - Warm-up runs documented
   - N ≥ 30 runs (or stability criterion)
   - Report: median, p95, min, max
   - Machine: chip, OS, RAM, compiler, flags
3. **Correctness proof**
   - Golden reference
   - Explicit tolerance (abs, rel, or ULP)
   - Max observed error
4. **Explanation**
   - Why the optimization worked (or didn't)
   - What is the bottleneck
   - Roofline classification where relevant

### Evidence Collection Template

```markdown
## Measurement Protocol

- **Input:** N=1024, random seed=42
- **Warm-up:** 5 runs discarded
- **Measured runs:** 50
- **Machine:** MacBook Air M4, macOS 15.x, 16GB RAM
- **Compiler:** Apple clang 16.0, -O3 -march=native
- **Date:** 2026-11-01

## Results

| Metric | Baseline | Optimized |
|--------|----------|-----------|
| Median (ms) | 142.3 | 28.7 |
| p95 (ms) | 144.1 | 29.2 |
| Speedup | — | 4.96× |

## Correctness

- Golden: scalar_reference.bin
- Tolerance: 1e-5 relative
- Max error: 3.2e-6
- Pass: YES

## Analysis

The speedup comes from NEON vectorization of the inner loop.
4-wide f32 vectors match the theoretical 4× improvement.
```

---

## 5. Repository Structure

```
forge/
├── README.md                 # Project choice and overview
├── CMakeLists.txt           # Build system
├── src/
│   ├── gemm_scalar.cpp      # F0 baseline
│   ├── gemm_neon.cpp        # F1 SIMD
│   ├── gemm_tiled.cpp       # F2 optimized
│   ├── gemm.metal           # F3 GPU
│   └── gemm_quant.cpp       # F4 quantized
├── tests/
│   ├── test_correctness.cpp # Golden comparison
│   ├── golden/              # Reference outputs
│   └── vectors/             # Test inputs
├── bench/
│   ├── benchmark.cpp        # Measurement harness
│   └── results/             # Saved measurements
└── docs/
    └── roofline.md          # F2 analysis
```

---

## 6. Grading Rubric

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Correctness** | 30% | All stages pass golden tests |
| **Measurement** | 25% | Proper protocol, reproducible |
| **Explanation** | 25% | Understands why, not just what |
| **Progression** | 15% | Each stage builds on previous |
| **Documentation** | 5% | Clear, complete artifacts |

### Per-Stage Scores

| Stage | Points | Cumulative |
|-------|--------|------------|
| F0 | 15 | 15 |
| F1 | 20 | 35 |
| F2 | 20 | 55 |
| F3 | 25 | 80 |
| F4 | 20 | 100 |
| F5 | +10 | 110 (bonus) |

---

## 7. Anti-Patterns (Automatic Fail)

1. **No golden comparison** — Speed without correctness is theater
2. **Invented numbers** — Fabricated benchmarks
3. **Single run** — No statistical validity
4. **Hidden environment** — Not documenting machine/flags
5. **Claiming SVE on M4** — Hardware doesn't exist
6. **Claiming CUDA on M4** — Wrong GPU API
7. **Skipping stages** — F3 without F0-F2 complete
8. **Different problems per stage** — Must be same mathematical motif

---

## 8. FAQ

**Q: Can I use a different project than GEMM/FIR/Jacobi?**
A: Yes, but clear it first. The project must be dense enough to benefit from SIMD, have clear Roofline characteristics, and translate to GPU. Trivial kernels don't qualify.

**Q: Do I need FPGA hardware for F5?**
A: No. Option C (honest stop) is valid. RTL can be simulated.

**Q: What if GPU is slower than CPU for my kernel?**
A: Document it! Understanding why is more valuable than faking a speedup.

**Q: Can I use libraries (Accelerate, vDSP, Metal Performance Shaders)?**
A: For comparison, yes. But you must have your own implementation to show understanding.

**Q: What N sizes should I test?**
A: Document at least 3 sizes that show different behavior (e.g., fits L1, fits L2, exceeds L3).

---

## 9. Definition of Done

- [ ] Project choice documented in `forge/README.md`
- [ ] F0-F4 stages complete with artifacts
- [ ] All golden tests pass
- [ ] Measurement protocol documented per stage
- [ ] Roofline analysis present (F2)
- [ ] GPU implementation with transfer costs (F3)
- [ ] Quantized version with error analysis (F4)
- [ ] F5 present as complete OR honest stop documented
- [ ] Study log artifacts linked from Forge rooms
