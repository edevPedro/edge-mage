# CHANGELOG — Neurotech gamification P0

Make the Neurotech circle feel gameful (Edge-parity loop), not a thin complement.

## Landed

- **`NEURO_RANKS`** + `effective_neuro_rank` — Novice → Signal Adept → Decode Adept → Closed-Loop Adept → Neuro Mage (rune + boss gated; never Edge XP / on-device)
- **Real rune inventory** in `progress.runes`: `rune-neuro-acq` @ filter-bank (or electrode chain), `rune-neuro-decode` @ decode-mvp, `rune-neuro-online` @ online-stub
- **Boss gate**: `nt-neuro-mage` requires 3 runas + online + paper\|project; title Neuro Mage needs ritual
- **HUD**: home / profile / statusline / `:xp` course-aware when `--course neurotech` (`◈runas · mage · %fases`)
- **Ceremony**: milestone splash + rune drop banners on filter / decode / online / boss
- **Grimório** copy aligned with real drops
- **Tests**: ranks, rune persist, boss unlock, Edge ladder isolation
- **Web (edevs)**: progresso panel (rooms % + runas) on `/estudo/cursos/neurotech`; API `neurotech` slice on mage progress

## Parallel circle (unchanged hard rules)

- Neurotech runes / Neuro Mage **do not** gate Mago Supremo
- Educational BCI only
