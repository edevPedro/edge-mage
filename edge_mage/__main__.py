"""Entrypoint: python -m edge_mage | mage | emage | edge-mage."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="mage",
        description="e-mage — TUI academy (Fundamentals · Systems · Edge · Performance · Neurotech).",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="e-mage 0.3.0",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=[
            "sync", "courses", "emu", "publish", "lab",
            "today", "verify", "close", "week", "roadmap", "init", "workdir", "branch", "chart",
        ],
        help="Optional: sync | courses | emu | publish <boss> | lab … | today | verify | close | week | roadmap | init | workdir | branch | chart",
    )
    parser.add_argument(
        "--course",
        choices=["fundamentals", "systems", "edge", "performance", "neurotech"],
        default=None,
        help="Skip launcher and open a course directly",
    )
    parser.add_argument(
        "--today",
        action="store_true",
        help="Open the TUI directly on the Hoje (today) screen",
    )
    parser.add_argument(
        "arg",
        nargs=argparse.REMAINDER,
        help="Args for `emu`/`publish`/`lab` or flags for `verify`/`close`/`init`",
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

    if args.command in ("today", "verify", "close", "week", "roadmap", "init", "workdir", "branch", "chart"):
        from edge_mage.roadmap.cli import main as daily_main

        sys.exit(daily_main([args.command, *args.arg]))

    if args.command == "publish":
        from edge_mage.publish import known_bosses, publish_boss, status_report

        if not args.arg:
            print(status_report())
            print(f"\nuso: mage publish <boss>   #{', '.join(known_bosses())}")
            sys.exit(0)
        result = publish_boss(args.arg[0])
        print(result.message)
        if result.next_steps:
            print("\nPróximos passos:")
            for step in result.next_steps:
                print(f"  - {step}")
        sys.exit(0 if result.ok else 1)

    from edge_mage.app import run

    show_launcher = args.course is None and args.command != "courses"
    if args.command == "courses":
        show_launcher = True
        course = None
    else:
        course = args.course
        show_launcher = course is None
    run(course=course, show_launcher=show_launcher, open_today=args.today)


if __name__ == "__main__":
    main()
