"""CLI: python -m edge_mage.emulators <synth|artifact|cortex|thumb2|spice|viz|latency|online|spike|ecog|neuromod|stim|all>"""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(
        prog="python -m edge_mage.emulators",
        description="Neurotech educational emulators (synth EEG · artifacts · Cortex-M stub · invasive/neuromod stubs)",
    )
    p.add_argument(
        "which",
        nargs="?",
        default="all",
        choices=[
            "synth",
            "artifact",
            "cortex",
            "thumb2",
            "spice",
            "viz",
            "latency",
            "online",
            "spike",
            "ecog",
            "neuromod",
            "stim",
            "neuron",
            "all",
        ],
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
        print()
    if args.which in ("spike", "all"):
        try:
            from edge_mage.emulators.spike_stream import SpikeStream, SpikeStreamConfig
            s = SpikeStream(SpikeStreamConfig(seed=42))
            d = s.generate_window_ms(200.0, intention=0.7)
            print(f"[spike] mua={d['mua_count']} intent={d['intention']} lfp_ch={len(d['lfp_uv'])}")
        except Exception as e:
            print(f"spike demo err: {e}")
        print()
    if args.which in ("ecog", "all"):
        try:
            from edge_mage.emulators.ecog_stream import EcogStream, EcogConfig
            e = EcogStream(EcogConfig(seed=42))
            d = e.generate_window_ms(150.0, intention=0.6)
            print(f"[ecog] ch={d['n_ch']} grid={d['grid']} intent={d['intention']}")
        except Exception as e:
            print(f"ecog demo err: {e}")
        print()
    if args.which in ("neuromod", "all"):
        try:
            from edge_mage.emulators.neuromod_loop import NeuromodLoop, NMLConfig
            nl = NeuromodLoop(NMLConfig(beta_thresh=1.2, hysteresis=0.05))
            seq = nl.simulate_window(5)
            print(f"[neuromod] {seq}")
        except Exception as e:
            print(f"neuromod demo err: {e}")
        print()
    if args.which in ("stim", "all"):
        try:
            from edge_mage.emulators.stim_safety import StimSafetyStub, Pulse
            ss = StimSafetyStub()
            r = ss.analyze([Pulse(200, 1.0, 1), Pulse(200, 1.0, -1)], rate_hz=20)
            print(f"[stim] ok={r['ok']} imb={r['imbalance_pct']}% warn={r['warnings']}")
        except Exception as e:
            print(f"stim demo err: {e}")
        print()
    if args.which in ("neuron", "all"):
        try:
            from edge_mage.emulators.neuron_cli_stub import NeuronCLIStub, NeuronSimConfig
            n = NeuronCLIStub(NeuronSimConfig(tstop_ms=80.0))
            r = n.run_hh_sim(stim_amp_nA=6.0, stim_dur_ms=30.0)
            c = n.run_passive_cable(1500.0)
            print(f"[neuron] hh_spikes={r['spike_count']} tau_ms={c['tau_ms']} lambda_um={c['lambda_um']}")
        except Exception as e:
            print(f"neuron demo err: {e}")
        print()


if __name__ == "__main__":
    main()

