"""Entrypoint: python -m edge_mage | mage | emage | edge-mage."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="mage",
        description="e-mage — TUI academy (Fundamentals · Systems · Edge ML · Neurotech).",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="e-mage 0.2.0",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["sync", "courses", "emu"],
        help="Optional: sync | courses | emu (neurotech emulators)",
    )
    parser.add_argument(
        "--course",
        choices=["fundamentals", "systems", "edge", "neurotech"],
        default=None,
        help="Skip launcher and open a course directly",
    )
    parser.add_argument(
        "emu_which",
        nargs="?",
        default="all",
        choices=["synth", "artifact", "cortex", "all"],
        help="With `emu`: which emulator demo",
    )
    args = parser.parse_args(argv)

    if args.command == "sync":
        from edge_mage.sync import sync_all

        result = sync_all()
        print(result.message)
        if result.warning:
            print(result.warning, file=sys.stderr)
        sys.exit(0 if result.ok else 1)

    if args.command == "emu":
        from edge_mage.emulators.__main__ import main as emu_main

        emu_main([args.emu_which])
        sys.exit(0)

    from edge_mage.app import run

    show_launcher = args.course is None and args.command != "courses"
    if args.command == "courses":
        show_launcher = True
        course = None
    else:
        course = args.course
        show_launcher = course is None
    run(course=course, show_launcher=show_launcher)


if __name__ == "__main__":
    main()
