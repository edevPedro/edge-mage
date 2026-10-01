"""Lista de salas de uma trilha."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.models import Track
from edge_mage.screens.base import MageScreen


class RoomListScreen(MageScreen):
    list_id = "room-list"

    def __init__(self, track: Track) -> None:
        super().__init__()
        self.track = track
        self.context_label = f"tracks/{track.id}"

    def compose_body(self) -> ComposeResult:
        store = self.app.store  # type: ignore[attr-defined]
        with Vertical():
            yield Static(f"{self.track.icon}  {self.track.title}", classes="title")
            yield Static(self.track.summary, classes="muted")
            options: list[Option] = []
            for room in self.track.rooms:
                unlocked = store.is_room_unlocked(self.track, room)
                done, total = store.room_progress(self.track.id, room)
                finished = store.is_room_done(self.track.id, room.id)
                mark = "✓" if finished else "·"
                label = f"{mark}  {room.title}"
                if not unlocked:
                    label += f"  🔒 {room.unlock_xp} XP"
                else:
                    label += f"  ({done}/{total} tasks · +{room.xp_reward} XP sala)"
                options.append(Option(label, id=room.id))
            yield OptionList(*options, id="room-list")

    def on_mount(self) -> None:
        super().on_mount()
        if hasattr(self.app, "set_nav_context"):
            self.app.set_nav_context(self.context_label)  # type: ignore[attr-defined]
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        room_id = str(event.option.id)
        room = next(r for r in self.track.rooms if r.id == room_id)
        store = self.app.store  # type: ignore[attr-defined]
        if not store.is_room_unlocked(self.track, room):
            self.notify(
                f"Sala bloqueada — precisa de {room.unlock_xp} XP",
                severity="warning",
            )
            return
        from edge_mage.screens.room import RoomScreen

        self.app.push_screen(RoomScreen(self.track, room))
