"""Lista de trilhas."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.models import Track
from edge_mage.screens.base import MageScreen


class TracksScreen(MageScreen):
    context_label = "tracks"
    list_id = "track-list"

    def compose_body(self) -> ComposeResult:
        app = self.app
        store = app.store  # type: ignore[attr-defined]
        tracks: list[Track] = app.tracks  # type: ignore[attr-defined]
        self._tracks = tracks

        with Vertical():
            yield Static("TRILHAS DA ACADEMIA", classes="title")
            yield Static(
                "j/k navegar · Enter/l abrir · :room <id> · Esc/h voltar",
                classes="muted",
            )
            options: list[Option] = []
            for track in tracks:
                unlocked = store.is_track_unlocked(track)
                done, total = store.track_progress(track)
                label = f"{track.icon}  {track.title}"
                if not unlocked:
                    label += f"  🔒 {track.unlock_xp} XP"
                elif done == total and total > 0:
                    label += f"  ✓ {done}/{total}"
                else:
                    label += f"  {done}/{total} salas"
                options.append(Option(label, id=track.id))
            yield OptionList(*options, id="track-list")

    def on_mount(self) -> None:
        super().on_mount()
        if hasattr(self.app, "set_nav_context"):
            self.app.set_nav_context("tracks")  # type: ignore[attr-defined]
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        track_id = str(event.option.id)
        track = next(t for t in self._tracks if t.id == track_id)
        store = self.app.store  # type: ignore[attr-defined]
        if not store.is_track_unlocked(track):
            self.notify(
                f"Trilha bloqueada — precisa de {track.unlock_xp} XP",
                severity="warning",
            )
            return
        from edge_mage.screens.room_list import RoomListScreen

        self.app.push_screen(RoomListScreen(track))
