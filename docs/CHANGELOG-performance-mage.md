# Changelog — Performance Mage

## 2026-11-02 — Course scaffold

- Added course id **`performance`** to TUI catalog, launcher, and `mage --course performance`.
- New track `content/tracks/11-performance/` — 20 rooms (F0→F6): architecture, NEON, numerical/Roofline, Metal(+CUDA elective), inference bridge, co-design.
- Performance Boss ritual documented in `docs/SPEC-performance-mage.md` + boss rooms (`pf-boss-arm-math`, `pf-boss-physics`, `pf-boss-metal`, `pf-boss-accelerator`).
- Explicit **non-gate**: Performance is not required for Edge ML / Mago Supremo; soft modular deps only.
- M4 caveats in SPEC + portal room (µarch, no SVE, Metal≠CUDA).
- Web stub: edevs `content/estudo/performance/export.json` + course card.
- Tests: `tests/test_performance.py`.
