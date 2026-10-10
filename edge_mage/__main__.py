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
        choices=["sync", "courses", "emu", "lab"],
        help="Optional: sync | courses | emu | lab list|init|run|latest",
    )
    parser.add_argument(
        "--course",
        choices=["fundamentals", "systems", "edge", "neurotech"],
        default=None,
        help="Skip launcher and open a course directly",
    )
    parser.add_argument(
        "arg",
        nargs="*",
        default=[],
        help="Args for `emu` (which) or `lab` (list|init|run|latest <id>)",
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

        emu_main([args.arg[0] if args.arg else "all"])
        sys.exit(0)

    if args.command == "lab":
        from edge_mage.labs.cli import main as lab_main

        sys.exit(lab_main(args.arg))

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
