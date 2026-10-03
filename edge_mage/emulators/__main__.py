"""CLI: python -m edge_mage.emulators <synth|artifact|cortex|all>"""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(
        prog="python -m edge_mage.emulators",
        description="Neurotech educational emulators (synth EEG · artifacts · Cortex-M stub)",
    )
    p.add_argument(
        "which",
        nargs="?",
        default="all",
        choices=["synth", "artifact", "cortex", "thumb2", "spice", "viz", "latency", "online", "all"],
        help="Which emulator demo to run",
    )
    p.add_argument("--seconds", type=float, default=1.0, help="synth duration")
    args = p.parse_args(argv)

    if args.which in ("synth", "all"):
        from edge_mage.emulators.synth_eeg import _demo as synth_demo

        synth_demo(seconds=args.seconds, with_mu=True)
        print()
    if args.which in ("artifact", "all"):
        from edge_mage.emulators.artifact_inject import _demo as art_demo

        art_demo()
        print()
    if args.which in ("cortex", "all"):
        from edge_mage.emulators.cortex_m_stub import _demo as cortex_demo

        cortex_demo()
        print()
    if args.which in ("thumb2", "all"):
        from edge_mage.emulators.cortex_m_emu import _demo as thumb2_demo

        thumb2_demo()
        print()
    if args.which in ("spice", "all"):
        from edge_mage.emulators.spice_lite import _demo as spice_demo

        spice_demo()
        print()
    if args.which in ("viz", "all"):
        from edge_mage.emulators.signal_viz import _demo as viz_demo

        viz_demo()
        print()
    if args.which in ("latency", "all"):
        from edge_mage.emulators.latency_budget import _demo as lat_demo

        lat_demo()
        print()
    if args.which in ("online", "all"):
        from edge_mage.emulators.online_loop import _demo as online_demo

        online_demo()


if __name__ == "__main__":
    main(sys.argv[1:])
