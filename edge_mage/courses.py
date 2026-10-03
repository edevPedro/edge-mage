"""Course catalog for e-mage launcher (fundamentals / systems / edge / neurotech)."""

from __future__ import annotations

from dataclasses import dataclass


COURSE_FUNDAMENTALS = "fundamentals"
COURSE_SYSTEMS = "systems"
COURSE_EDGE = "edge"
COURSE_NEUROTECH = "neurotech"

# Soft gate: Systems + Edge + Neurotech prefer Mago base; preview allowed with warning.
GATED_COURSES = frozenset({COURSE_SYSTEMS, COURSE_EDGE, COURSE_NEUROTECH})


@dataclass(frozen=True)
class CourseInfo:
    id: str
    title: str
    title_pt: str
    blurb: str
    requires_mago_base: bool = False


COURSES: tuple[CourseInfo, ...] = (
    CourseInfo(
        COURSE_FUNDAMENTALS,
        "Fundamentals",
        "Fundamentos",
        "Path to Mago base — shared core + tutorial rooms.",
        requires_mago_base=False,
    ),
    CourseInfo(
        COURSE_SYSTEMS,
        "Systems Mage",
        "Systems Mage",
        "FLAG catalog offline (systems + llvm + math); sync refreshes pack.",
        requires_mago_base=True,
    ),
    CourseInfo(
        COURSE_EDGE,
        "Edge ML Mage",
        "Edge ML Mage",
        "Current TUI tracks: math → on-device Edge AI.",
        requires_mago_base=True,
    ),
    CourseInfo(
        COURSE_NEUROTECH,
        "Neurotech",
        "Neurotech",
        "Círculo paralelo BCI/EEG — Estuda → Sala; não gateia Mago Supremo.",
        requires_mago_base=True,
    ),
)


def course_by_id(course_id: str) -> CourseInfo | None:
    for c in COURSES:
        if c.id == course_id:
            return c
    return None
