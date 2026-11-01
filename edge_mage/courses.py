"""Course / journey catalog for e-mage launcher.

Primary UX: one continuous journey (`emage`).
Legacy ids remain as a secondary module browser.
"""

from __future__ import annotations

from dataclasses import dataclass


COURSE_EMAGE = "emage"
COURSE_FUNDAMENTALS = "fundamentals"
COURSE_SYSTEMS = "systems"
COURSE_EDGE = "edge"
COURSE_PERFORMANCE = "performance"
COURSE_NEUROTECH = "neurotech"

# Soft gate: specialization / advanced modules prefer Mago base; preview allowed.
GATED_COURSES = frozenset(
    {
        COURSE_SYSTEMS,
        COURSE_EDGE,
        COURSE_PERFORMANCE,
        COURSE_NEUROTECH,
        COURSE_EMAGE,  # soft: preview beyond P0 with warning
    }
)

# Shown in the secondary “module browser” (not competing primary picks).
MODULE_BROWSER_IDS = frozenset(
    {
        COURSE_FUNDAMENTALS,
        COURSE_SYSTEMS,
        COURSE_EDGE,
        COURSE_PERFORMANCE,
        COURSE_NEUROTECH,
    }
)


@dataclass(frozen=True)
class CourseInfo:
    id: str
    title: str
    title_pt: str
    blurb: str
    requires_mago_base: bool = False
    primary: bool = False
    elective: bool = False


# Primary journey first; then module browser aliases (legacy course ids).
COURSES: tuple[CourseInfo, ...] = (
    CourseInfo(
        COURSE_EMAGE,
        "e-mage Journey",
        "Jornada e-mage",
        "One path: systems → arch → SIMD → HPC → GPU → inference → co-design.",
        requires_mago_base=False,
        primary=True,
    ),
    CourseInfo(
        COURSE_FUNDAMENTALS,
        "Module · Foundations",
        "Módulo · Fundamentos",
        "P0 literacy → Mago base (module browser).",
        requires_mago_base=False,
    ),
    CourseInfo(
        COURSE_SYSTEMS,
        "Module · Systems",
        "Módulo · Systems",
        "P1 FLAG catalog (systems + llvm + math + craft).",
        requires_mago_base=True,
    ),
    CourseInfo(
        COURSE_PERFORMANCE,
        "Module · Performance phases",
        "Módulo · Fases Performance",
        "P2–P5/P7 NEON/Roofline/Metal/co-design (alias of spine phases).",
        requires_mago_base=True,
    ),
    CourseInfo(
        COURSE_EDGE,
        "Module · Inference / Edge ML",
        "Módulo · Inferência / Edge ML",
        "P6 on-device path (math → export → CMSIS → ritual).",
        requires_mago_base=True,
    ),
    CourseInfo(
        COURSE_NEUROTECH,
        "Branch · Neurotech",
        "Ramo · Neurotech",
        "Optional BCI/EEG circle — not a competing main course.",
        requires_mago_base=True,
        elective=True,
    ),
)


def course_by_id(course_id: str) -> CourseInfo | None:
    for c in COURSES:
        if c.id == course_id:
            return c
    return None


def primary_course() -> CourseInfo:
    for c in COURSES:
        if c.primary:
            return c
    return COURSES[0]
