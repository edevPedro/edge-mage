"""Entrypoint: python -m edge_mage | edge-mage | emage | mage."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="edge-mage",
        description="Edge Mage — academia TUI (math → Edge AI).",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="edge-mage 0.1.0",
    )
    parser.parse_args(argv)
    from edge_mage.app import run

    run()


if __name__ == "__main__":
    main()
