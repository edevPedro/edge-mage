"""Ordem pedagógica e 'continuar' (uma porta brilhante)."""

from __future__ import annotations

from edge_mage.models import Room, Track


def pedagogical_rooms(tracks: list[Track]) -> list[tuple[Track, Room]]:
    """Salas na ordem CURRICULUM (track.order, depois dir/ordem de rooms)."""
    ordered = sorted(tracks, key=lambda t: t.order)
    out: list[tuple[Track, Room]] = []
    for t in ordered:
        if t.scaffold:
            continue
        for r in t.rooms:
            out.append((t, r))
    return out


def next_open_room(store, tracks: list[Track]) -> tuple[Track, Room] | None:
    """Próxima sala pedagoógica ainda não concluída e desbloqueada."""
    for track, room in pedagogical_rooms(tracks):
        if store.is_room_done(track.id, room.id):
            continue
        if not store.is_room_unlocked(track, room):
            continue
        return track, room
    # fallback: primeira incompleta mesmo bloqueada (para mensagem)
    for track, room in pedagogical_rooms(tracks):
        if not store.is_room_done(track.id, room.id):
            return track, room
    return None


def continue_label(store, tracks: list[Track]) -> str:
    nxt = next_open_room(store, tracks)
    if nxt is None:
        return "▶  Continuar — currículo completo"
    track, room = nxt
    locked = not store.is_room_unlocked(track, room)
    mark = "🔒 " if locked else "▶  "
    return f"{mark}Continuar · {room.title}"
