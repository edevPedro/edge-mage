"""Neurotech MSc-prep course: load, pillars path, emulators, Supremo route."""

from __future__ import annotations

from edge_mage.animations.math import animation_for_room, render_frame
from edge_mage.content import load_tracks_for_course
from edge_mage.courses import COURSE_EDGE, COURSE_NEUROTECH, COURSES
from edge_mage.emulators import (
    CortexMPipelineStub,
    SynthEEGStream,
    inject_artifacts,
    run_online_stub,
    stage_budget,
)
from edge_mage.emulators.artifact_inject import detect_line_power
from edge_mage.models import Task, Track
from edge_mage.progress import ProgressStore
from edge_mage.validators import validate_task

# Full pedagogical chain (65 required + 3 electives = 68).
PEDAGOGICAL_IDS = [
    "nt-portal",
    "nt-ethics-consent",
    "nt-math-vectors",
    "nt-math-matrices",
    "nt-math-eigen",
    "nt-math-probability",
    "nt-math-estimation",
    "nt-math-gd-lite",
    "nt-dipole-scalp",
    "nt-physics-rc-tissue",
    "nt-spike-lfp",
    "nt-volume-blur",
    "nt-physics-field-lite",
    "nt-electrode-snr",
    "nt-ground-ref",
    "nt-elec-opamp-noise",
    "nt-adc-bio",
    "nt-elec-antialias",
    "nt-neuro-neuron-hh",
    "nt-neuro-synapse",
    "nt-rhythms",
    "nt-neuro-maps",
    "nt-neuro-plasticity",
    "nt-cs-complexity",
    "nt-cs-ringbuf-ds",
    "nt-cs-numerics",
    "nt-cs-harness",
    "nt-filter-bank",
    "nt-dsp-welch",
    "nt-filter-design-depth",
    "nt-artifacts",
    "nt-mi-paradigm",
    "nt-features-bandpower",
    "nt-trial-design",
    "nt-stats-bci",
    "nt-hypothesis-power",
    "nt-cv-leakage",
    "nt-decode-mvp",
    "nt-csp-primer",
    "nt-riemann-primer",
    "nt-metrics-offline",
    "nt-ml-neural",
    "nt-stream-buffer",
    "nt-fw-irq-dma",
    "nt-mcu-filter",
    "nt-fw-fixedpoint",
    "nt-fw-aarch64-bridge",
    "nt-latency-budget",
    "nt-online-stub",
    "nt-closed-loop-control",
    "nt-checkpoint-paper",
    "nt-checkpoint-project",
    "nt-neuro-mage",
    "nt-app-assistive-bci",
    "nt-app-neurofeedback",
    "nt-app-hybrid-p300",
    "nt-case-berlin-mi",
    "nt-case-bci-comp-iv",
    "nt-irb-protocol",
    "nt-paper-critique",
    "nt-research-proposal",
    "nt-thesis-methods",
    "nt-research-project",
    "nt-paper-module-msc",
    "nt-mago-supremo",
    "nt-ssvep-elective",
    "nt-fbcsp-bakeoff",
    "nt-openbci-path",
]

REQUIRED_IDS = PEDAGOGICAL_IDS[:65]
ELECTIVE_IDS = PEDAGOGICAL_IDS[65:]


def _neuro_track() -> Track:
    tracks = load_tracks_for_course(COURSE_NEUROTECH)
    assert len(tracks) == 1
    return tracks[0]


def test_neurotech_in_catalog() -> None:
    assert any(c.id == COURSE_NEUROTECH for c in COURSES)


def test_neurotech_pedagogical_order_locked() -> None:
    track = _neuro_track()
    ids = [r.id for r in track.rooms]
    assert ids == PEDAGOGICAL_IDS
    assert [r.order for r in track.rooms] == list(range(1, 69))
    assert len(REQUIRED_IDS) == 65
    assert len(ELECTIVE_IDS) == 3


def test_msc_path_length_and_pillars() -> None:
    track = _neuro_track()
    by_id = {r.id: r for r in track.rooms}
    # Foundations present
    for rid in (
        "nt-math-vectors",
        "nt-physics-rc-tissue",
        "nt-elec-opamp-noise",
        "nt-neuro-neuron-hh",
        "nt-cs-ringbuf-ds",
        "nt-fw-irq-dma",
        "nt-app-hybrid-p300",
        "nt-case-berlin-mi",
        "nt-mago-supremo",
    ):
        assert rid in by_id
    assert by_id["nt-mago-supremo"].boss is True
    # Published-case rooms cite real sources
    berlin = by_id["nt-case-berlin-mi"]
    assert any("pmc" in (r.url or "").lower() or "doi.org" in (r.url or "").lower() for r in berlin.resources)


def test_f2_requires_rooms_chain() -> None:
    track = _neuro_track()
    by_id = {r.id: r for r in track.rooms}
    assert by_id["nt-ground-ref"].requires_rooms == ["nt-electrode-snr"]
    assert "nt-cs-harness" in by_id["nt-filter-bank"].requires_rooms
    assert "nt-rhythms" in by_id["nt-filter-bank"].requires_rooms


def test_f6_gates_online_xor_boss() -> None:
    track = _neuro_track()
    by_id = {r.id: r for r in track.rooms}
    assert by_id["nt-checkpoint-paper"].requires_rooms == ["nt-online-stub"]
    assert by_id["nt-checkpoint-project"].requires_rooms == ["nt-online-stub"]
    boss = by_id["nt-neuro-mage"]
    assert "nt-online-stub" in boss.requires_rooms
    assert set(boss.requires_rooms_any) == {
        "nt-checkpoint-paper",
        "nt-checkpoint-project",
    }


def test_requires_rooms_enforced_in_unlock(tmp_path) -> None:
    track = _neuro_track()
    store = ProgressStore(tmp_path / "neuro-progress.json")
    portal = next(r for r in track.rooms if r.id == "nt-portal")
    ethics = next(r for r in track.rooms if r.id == "nt-ethics-consent")
    math_v = next(r for r in track.rooms if r.id == "nt-math-vectors")
    ground = next(r for r in track.rooms if r.id == "nt-ground-ref")
    assert store.is_room_unlocked(track, portal)
    assert not store.is_room_unlocked(track, ethics)
    store.state.completed_rooms_by_id["nt-portal"] = True
    assert store.is_room_unlocked(track, ethics)
    assert not store.is_room_unlocked(track, math_v)
    assert not store.is_room_unlocked(track, ground)

    # Neuro Mage needs online + (paper OR project) + 3 neuro runes
    boss = next(r for r in track.rooms if r.id == "nt-neuro-mage")
    store.state.completed_rooms_by_id["nt-online-stub"] = True
    store.state.completed_rooms_by_id["nt-closed-loop-control"] = True
    assert not store.is_room_unlocked(track, boss)
    store.state.completed_rooms_by_id["nt-checkpoint-paper"] = True
    assert not store.is_room_unlocked(track, boss)
    store.state.completed_rooms_by_id["nt-filter-bank"] = True
    store.state.completed_rooms_by_id["nt-decode-mvp"] = True
    assert store.is_room_unlocked(track, boss)


def test_supremo_boss_requires_research_rune(tmp_path) -> None:
    from edge_mage.ranks import NEURO_RUNE_RESEARCH

    track = _neuro_track()
    store = ProgressStore(tmp_path / "sup.json")
    climax = next(r for r in track.rooms if r.id == "nt-mago-supremo")
    # Satisfy room gates except research project (also drops research rune).
    for rid in climax.requires_rooms:
        if rid != "nt-research-project":
            store.state.completed_rooms_by_id[rid] = True
    store.state.rituals["neuro-mage"] = True
    store.state.completed_rooms_by_id["nt-filter-bank"] = True
    store.state.completed_rooms_by_id["nt-decode-mvp"] = True
    store.state.completed_rooms_by_id["nt-online-stub"] = True
    store.sync_neuro_runes_from_rooms()
    assert not store.has_rune(NEURO_RUNE_RESEARCH)
    assert not store.is_room_unlocked(track, climax)
    store.state.completed_rooms_by_id["nt-research-project"] = True
    store.sync_neuro_runes_from_rooms()
    assert store.has_rune(NEURO_RUNE_RESEARCH)
    assert store.is_room_unlocked(track, climax)


def test_edge_excludes_neurotech_track() -> None:
    edge = load_tracks_for_course(COURSE_EDGE)
    assert all(t.id != "neurotech" for t in edge)
    assert all(t.course != COURSE_NEUROTECH for t in edge)


def test_neuro_ranks_and_runes() -> None:
    from edge_mage.ranks import (
        NEURO_RUNE_ACQ,
        NEURO_RUNE_DECODE,
        NEURO_RUNE_ONLINE,
        NEURO_RUNE_RESEARCH,
        effective_neuro_rank,
        neuro_runes_earned_from_rooms,
    )

    assert effective_neuro_rank([NEURO_RUNE_ACQ], has_neuro_mage_boss=False).id == (
        "signal_adept"
    )
    assert (
        effective_neuro_rank(
            [NEURO_RUNE_ACQ, NEURO_RUNE_DECODE], has_neuro_mage_boss=False
        ).id
        == "decode_adept"
    )
    three = [NEURO_RUNE_ACQ, NEURO_RUNE_DECODE, NEURO_RUNE_ONLINE]
    assert effective_neuro_rank(three, has_neuro_mage_boss=False).id == "closed_loop_adept"
    assert effective_neuro_rank(three, has_neuro_mage_boss=True).id == "neuro_mage"
    assert effective_neuro_rank([], has_neuro_mage_boss=True).id == "neuro_novice"

    assert NEURO_RUNE_ACQ in neuro_runes_earned_from_rooms(
        {"nt-electrode-snr", "nt-ground-ref", "nt-adc-bio"}
    )
    assert NEURO_RUNE_DECODE in neuro_runes_earned_from_rooms({"nt-decode-mvp"})
    assert NEURO_RUNE_ONLINE in neuro_runes_earned_from_rooms({"nt-online-stub"})
    assert NEURO_RUNE_RESEARCH in neuro_runes_earned_from_rooms({"nt-research-project"})


def test_neuro_mage_alone_not_supremo(tmp_path) -> None:
    store = ProgressStore(tmp_path / "runes.json")
    store.state.courses["fundamentals"] = {"cleared": True, "mago_base": True}
    store.state.completed_rooms_by_id["nt-filter-bank"] = True
    store.state.completed_rooms_by_id["nt-decode-mvp"] = True
    store.state.completed_rooms_by_id["nt-online-stub"] = True
    store.sync_neuro_runes_from_rooms()
    store.state.rituals["neuro-mage"] = True
    assert store.neuro_rank().id == "neuro_mage"
    assert store.global_rank().id != "mago_supremo"
    assert store.global_rank().id == "intermediate"


def test_neurotech_climax_grants_mago_supremo(tmp_path) -> None:
    store = ProgressStore(tmp_path / "supremo.json")
    store.state.courses["fundamentals"] = {"cleared": True, "mago_base": True}
    for rid in (
        "nt-filter-bank",
        "nt-decode-mvp",
        "nt-online-stub",
        "nt-research-project",
        "nt-paper-module-msc",
        "nt-mago-supremo",
        "nt-neuro-mage",
    ):
        store.state.completed_rooms_by_id[rid] = True
    store.state.rituals["neuro-mage"] = True
    store.state.rituals["neuro-supremo"] = True
    store.state.rituals["neuro-paper-module-msc"] = True
    store.sync_neuro_runes_from_rooms()
    assert store.has_neuro_supremo_path()
    assert store.global_rank().id == "mago_supremo"
    # Edge evidence not required on this route
    assert not store.has_ritual("on-device")


def test_edge_supremo_path_unchanged() -> None:
    from edge_mage.ranks import global_rank_from_flags

    assert (
        global_rank_from_flags(
            has_mago_base=True,
            has_systems_boss=True,
            has_edge_on_device=True,
            has_evidence=True,
        ).id
        == "mago_supremo"
    )
    assert (
        global_rank_from_flags(
            has_mago_base=True,
            has_neuro_supremo=True,
        ).id
        == "mago_supremo"
    )
    # Incomplete neuro path does not mint Supremo
    assert (
        global_rank_from_flags(
            has_mago_base=True,
            has_systems_boss=True,
            has_edge_on_device=False,
            has_evidence=True,
        ).id
        != "mago_supremo"
    )


def test_neuro_rune_drops_persist(tmp_path) -> None:
    from edge_mage.models import Room, Task
    from edge_mage.ranks import NEURO_RUNE_ACQ, NEURO_RUNE_DECODE, NEURO_RUNE_ONLINE

    store = ProgressStore(tmp_path / "runes.json")
    room = Room(
        id="nt-filter-bank",
        title="Filter",
        summary="",
        xp_reward=10,
        unlock_xp=0,
        lesson_md="",
        tasks=[Task(id="t1", type="mcq", prompt="?", xp=5, answer=0, choices=["a"])],
        path="",
        course="neurotech",
    )
    store.state.completed_tasks["neurotech/nt-filter-bank/t1"] = False
    result = store.mark_task("neurotech", "nt-filter-bank", "t1", 5, room)
    assert result["room_completed"]
    assert NEURO_RUNE_ACQ in result["newly_runes"]
    assert store.has_rune(NEURO_RUNE_ACQ)
    assert result["rank"].id == "signal_adept"
    assert result["milestone"] is True
    assert result["rank"].id != "novico"
    assert result["course"] == "neurotech"

    store.state.completed_rooms_by_id["nt-decode-mvp"] = True
    store.state.completed_rooms_by_id["nt-online-stub"] = True
    newly = store.sync_neuro_runes_from_rooms()
    assert NEURO_RUNE_DECODE in newly or store.has_rune(NEURO_RUNE_DECODE)
    assert store.has_rune(NEURO_RUNE_ONLINE)
    assert store.neuro_rank().id == "closed_loop_adept"

    store.state.rituals["neuro-mage"] = True
    assert store.neuro_rank().id == "neuro_mage"

    p = store.profile_summary("neurotech")
    assert p["rank"].id == "neuro_mage"
    assert p["runes_owned"] >= 3
    assert p["neuro_mage"] is True


def test_neuro_profile_not_edge_on_device(tmp_path) -> None:
    store = ProgressStore(tmp_path / "p.json")
    store.state.xp = 3000
    store.state.rituals["on-device"] = True
    edge = store.profile_summary("edge")
    assert edge["rank"].id == "edge_mage"
    neuro = store.profile_summary("neurotech")
    assert neuro["rank"].id == "neuro_novice"
    assert "on_device" in neuro
    assert neuro["runes_owned"] == 0


def test_synth_eeg_and_artifacts() -> None:
    stream = SynthEEGStream(n_channels=2, fs=250.0, seed=1)
    stream.schedule_mu_burst(
        start_sample=10, duration_samples=50, channel=0, amplitude=15.0, freq_hz=10.0
    )
    stream.schedule_mu_suppression(
        start_sample=80, duration_samples=40, channel=0, factor=0.2
    )
    block = stream.generate(200)
    assert len(block) == 200
    dirty = inject_artifacts(block, fs=250.0, kind="line", channel=0, amplitude=8.0)
    assert detect_line_power(dirty, 0, 250.0, 60.0) > detect_line_power(
        block, 0, 250.0, 60.0
    )


def test_cortex_m_stub_pipeline() -> None:
    mcu = CortexMPipelineStub(deadline_ms=40.0)
    result = mcu.process_window([0.1 * i for i in range(32)], taps=5)
    assert "packet_hex" in result
    assert result["miss"] is True


def test_latency_budget_and_online_loop() -> None:
    report = stage_budget(128.0, 3.0, 5.0, deadline_ms=40.0)
    assert report["miss"] is True
    out = run_online_stub(n_windows=4, deadline_ms=150.0)
    assert out["n_windows"] == 4


def test_neuro_animations_render() -> None:
    for kind in (
        "rhythm_bands",
        "filter_freq_response",
        "dipole_field",
        "spike_to_lfp",
        "mi_erds",
        "closed_loop_timeline",
        "volume_blur",
        "artifact_trace",
    ):
        assert animation_for_room("nt-x", kind) == kind
        frame = render_frame(kind, 0.25)
        assert len(frame) > 20


def test_estuda_files_present() -> None:
    track = _neuro_track()
    for room in track.rooms:
        assert room.lesson_md.strip(), room.id
        assert room.story_md.strip(), room.id
        assert room.concept_md.strip(), room.id


def test_substantive_rooms_have_http_resources() -> None:
    track = _neuro_track()
    for room in track.rooms:
        if room.order < 3:
            continue
        assert room.resources, f"{room.id} missing resources"
        assert any(r.url.startswith("http") for r in room.resources), room.id


def test_decode_mvp_lda_code_task() -> None:
    room = next(r for r in _neuro_track().rooms if r.id == "nt-decode-mvp")
    task = next(t for t in room.tasks if t.id == "lda-code")
    code = (
        "def predict_lda(x, w, b):\n"
        "    s = sum(a * b_ for a, b_ in zip(x, w)) + b\n"
        "    return 1 if s >= 0 else 0\n"
    )
    ok, msg = validate_task(task, code)
    assert ok, msg
