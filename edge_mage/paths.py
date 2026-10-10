"""Home dirs for e-mage: ~/.mage/ with one-time migrate from ~/.edge-mage/."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

LEGACY_HOME_NAME = ".edge-mage"
MAGE_HOME_NAME = ".mage"


def mage_home() -> Path:
    """
    Return ~/.mage/, creating it if needed.

    One-time: if ~/.mage is missing and ~/.edge-mage exists, copy the tree.
    Override with MAGE_HOME.
    """
    override = os.environ.get("MAGE_HOME", "").strip()
    if override:
        home = Path(override).expanduser()
        home.mkdir(parents=True, exist_ok=True)
        return home

    home = Path.home() / MAGE_HOME_NAME
    legacy = Path.home() / LEGACY_HOME_NAME
    if not home.exists() and legacy.exists() and legacy.is_dir():
        try:
            shutil.copytree(legacy, home)
        except OSError:
            home.mkdir(parents=True, exist_ok=True)
    else:
        home.mkdir(parents=True, exist_ok=True)
    return home


def packs_dir() -> Path:
    d = mage_home() / "packs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def progress_path() -> Path:
    return mage_home() / "progress.json"


def auth_path() -> Path:
    return mage_home() / "auth.json"


def config_path() -> Path:
    return mage_home() / "config.json"


def repo_root() -> Path:
    """Repository root (parent of the edge_mage package), used for roadmap/ and challenges/."""
    here = Path(__file__).resolve().parent.parent
    if (here / "roadmap").exists() or (here / "content").exists():
        return here
    return Path.cwd()


def roadmap_dir() -> Path:
    override = os.environ.get("MAGE_ROADMAP_ROOT", "").strip()
    if override:
        return Path(override).expanduser()
    return repo_root() / "roadmap"


def challenges_dir() -> Path:
    override = os.environ.get("MAGE_CHALLENGES_ROOT", "").strip()
    if override:
        return Path(override).expanduser()
    return repo_root() / "challenges"


def practice_dir() -> Path:
    """Default location for challenge working dirs (public artifact repos)."""
    override = os.environ.get("MAGE_WORK_ROOT", "").strip()
    if override:
        p = Path(override).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return p
    p = Path.home() / "mage-work"
    p.mkdir(parents=True, exist_ok=True)
    return p


def evidence_dir() -> Path:
    """Evidence log root for verifiable labs/challenges: ~/.mage/evidence/."""
    d = mage_home() / "evidence"
    d.mkdir(parents=True, exist_ok=True)
    return d


def daily_path() -> Path:
    """Daily state (active challenge, rollovers, closed days): ~/.mage/daily.json."""
    return mage_home() / "daily.json"


def labs_work_dir(lab_id: str) -> Path:
    """Student working directory for a lab: ~/.mage/labs/<id>/work/."""
    d = mage_home() / "labs" / lab_id / "work"
    d.mkdir(parents=True, exist_ok=True)
    return d


def legacy_home() -> Path:
    return Path.home() / LEGACY_HOME_NAME
