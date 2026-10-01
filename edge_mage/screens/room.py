"""Vista de sala: lição + animação + lista de tasks."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Markdown, OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.animations.math import animation_for_room
from edge_mage.models import Room, Track
from edge_mage.screens.base import MageScreen
from edge_mage.widgets.animation_panel import AnimationPanel


class RoomScreen(MageScreen):
    list_id = "task-list"

    def __init__(self, track: Track, room: Room) -> None:
        super().__init__()
        self.track = track
        self.room = room
        self.context_label = f"{track.id}/{room.id}"
        self.anim_kind = animation_for_room(room.id, room.animation)

    def compose_body(self) -> ComposeResult:
        store = self.app.store  # type: ignore[attr-defined]
        done, total = store.room_progress(self.track.id, self.room)
        has_anim = self.anim_kind != "none"
        with Vertical():
            yield Static(self.room.title, classes="title")
            hint = "  ·  Space/:anim visual" if has_anim else ""
            yield Static(
                f"{self.room.summary}  ·  progresso {done}/{total}{hint}",
                classes="muted",
            )
            with Horizontal(id="room-main"):
                with VerticalScroll(classes="panel", id="lesson", can_focus=False):
                    yield Static("LIÇÃO", classes="panel-title")
                    yield Markdown(self.room.lesson_md or "_Sem lição._")
                if has_anim:
                    panel = AnimationPanel(self.anim_kind, id="anim-panel")
                    panel.add_class("-hidden")
                    yield panel
            yield Static(
                "TAREFAS — j/k · Enter/l  ·  Esc/h voltar",
                classes="panel-title",
            )
            yield OptionList(*self._task_options(), id="task-list")

    def _task_options(self) -> list[Option]:
        store = self.app.store  # type: ignore[attr-defined]
        options: list[Option] = []
        for t in self.room.tasks:
            done = store.is_task_done(self.track.id, self.room.id, t.id)
            mark = "✓" if done else "○"
            kind = {"mcq": "MCQ", "numeric": "NUM", "fill": "FILL", "code": "CODE"}.get(
                t.type, t.type.upper()
            )
            label = (
                f"{mark}  [{kind}]  {t.prompt[:70]}"
                f"{'…' if len(t.prompt) > 70 else ''}  (+{t.xp} XP)"
            )
            options.append(Option(label, id=t.id))
        return options

    def on_mount(self) -> None:
        super().on_mount()
        if hasattr(self.app, "set_nav_context"):
            self.app.set_nav_context(self.context_label)  # type: ignore[attr-defined]
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]
        if self.anim_kind != "none":
            # Auto-play breve ao abrir a sala
            self.call_after_refresh(self._autoplay)

    def _autoplay(self) -> None:
        try:
            panel = self.query_one("#anim-panel", AnimationPanel)
        except Exception:
            return
        panel.play(self.anim_kind)

    def toggle_animation(self, kind: str | None = None) -> None:
        if self.anim_kind == "none" and not kind:
            self.app.notify("esta sala não tem visual", severity="warning")
            return
        try:
            panel = self.query_one("#anim-panel", AnimationPanel)
        except Exception:
            self.app.notify("painel de animação indisponível", severity="warning")
            return
        use = kind or self.anim_kind
        if kind:
            self.anim_kind = kind  # type: ignore[assignment]
        panel.toggle(use)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        task_id = str(event.option.id)
        task = next(t for t in self.room.tasks if t.id == task_id)
        from edge_mage.screens.task import TaskScreen

        self.app.push_screen(TaskScreen(self.track, self.room, task))

    def on_screen_resume(self) -> None:
        super().on_screen_resume()
        lst = self.query_one("#task-list", OptionList)
        lst.clear_options()
        lst.add_options(self._task_options())
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]
        self.focus_nav_target()
