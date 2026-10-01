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


def legacy_home() -> Path:
    return Path.home() / LEGACY_HOME_NAME
