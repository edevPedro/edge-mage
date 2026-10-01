"""Entrypoint: python -m edge_mage | mage | emage | edge-mage."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="mage",
        description="e-mage — TUI academy (Fundamentals · Systems · Edge ML).",
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
        choices=["sync", "courses"],
        help="Optional: sync (packs+progress) or courses (open launcher)",
    )
    parser.add_argument(
        "--course",
        choices=["fundamentals", "systems", "edge"],
        default=None,
        help="Skip launcher and open a course directly",
    )
    args = parser.parse_args(argv)

    if args.command == "sync":
        from edge_mage.sync import sync_all

        result = sync_all()
        print(result.message)
        if result.warning:
            print(result.warning, file=sys.stderr)
        sys.exit(0 if result.ok else 1)

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
