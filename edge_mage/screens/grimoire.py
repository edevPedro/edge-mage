"""Grimório — habilidades desbloqueadas ao concluir salas."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.screens.base import MageScreen


class GrimoireScreen(MageScreen):
    context_label = "grimório"
    list_id = "grimoire-actions"

    def compose_body(self) -> ComposeResult:
        app = self.app
        store = app.store  # type: ignore[attr-defined]
        skills = getattr(app, "skills", []) or []
        unlocked = []
        locked = []
        for s in skills:
            if store.is_skill_unlocked(s.id):
                unlocked.append(s)
            else:
                locked.append(s)

        lines_u = []
        for s in unlocked:
            lines_u.append(f"  {s.glyph}  {s.name}")
            lines_u.append(f"      {s.description}")
        if not lines_u:
            lines_u = ["  (nenhuma habilidade ainda — complete salas)"]

        lines_l = []
        for s in locked:
            where = s.unlock_room or "?"
            lines_l.append(f"  ·  {s.name}  —  sala `{where}`")
        if not lines_l:
            lines_l = ["  (todas desbloqueadas)"]

        with VerticalScroll(can_focus=False):
            yield Static("GRIMÓRIO DE HABILIDADES", classes="title")
            yield Static(
                f"Obtidas {len(unlocked)}/{len(skills)}  ·  "
                "cada sala concluída concede 1+ skills",
                classes="muted",
            )
            with Vertical(classes="panel"):
                yield Static("OBTIDAS", classes="panel-title")
                yield Static("\n".join(lines_u), classes="ok")
            with Vertical(classes="panel"):
                yield Static("SELADAS", classes="panel-title")
                yield Static("\n".join(lines_l), classes="locked")
            yield OptionList(Option("←  Voltar", id="back"), id="grimoire-actions")

    def on_mount(self) -> None:
        super().on_mount()
        if hasattr(self.app, "set_nav_context"):
            self.app.set_nav_context("grimório")  # type: ignore[attr-defined]
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if str(event.option.id) == "back":
            self.app.pop_screen()
