"""Resolver uma task — NORMAL (browse) vs INSERT (responder)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Input, OptionList, Static, TextArea
from textual.widgets.option_list import Option

from edge_mage.git_journal import journal_task_completion
from edge_mage.models import Room, Task, Track
from edge_mage.screens.base import MageScreen
from edge_mage.validators import validate_task


class TaskScreen(MageScreen):
    list_id = "task-actions"

    def __init__(self, track: Track, room: Room, quest: Task) -> None:
        super().__init__()
        self.track = track
        self.room = room
        self.quest = quest
        self.context_label = f"{track.id}/{room.id}/{quest.id}"

    def compose_body(self) -> ComposeResult:
        store = self.app.store  # type: ignore[attr-defined]
        done = store.is_task_done(self.track.id, self.room.id, self.quest.id)
        with Vertical():
            yield Static(
                f"TASK · {self.quest.type.upper()} · +{self.quest.xp} XP",
                classes="title",
            )
            yield Static(
                "NORMAL: j/k menu · i INSERT · Esc volta  ·  INSERT: digitar · Esc NORMAL",
                classes="muted",
            )
            with VerticalScroll(classes="panel", can_focus=False):
                yield Static(self.quest.prompt)
                if self.quest.type == "mcq" and self.quest.choices:
                    lines = []
                    for i, c in enumerate(self.quest.choices):
                        letter = chr(ord("A") + i)
                        lines.append(f"  {letter}) {c}")
                    yield Static("\n".join(lines), classes="accent")
                if self.quest.hint:
                    yield Static(f"Dica: {self.quest.hint}", classes="muted")
                if done:
                    yield Static(
                        "✓ Já concluída — pode refazer sem ganhar XP.",
                        classes="ok",
                    )

            if self.quest.type == "code":
                initial = self.quest.code_template or "# seu código aqui\n"
                yield TextArea(initial, id="answer", language="python")
            else:
                placeholder = {
                    "mcq": "A, B, C… ou 1, 2, 3…",
                    "numeric": "número (ex: 3.1416)",
                    "fill": "texto curto",
                }.get(self.quest.type, "resposta")
                yield Input(placeholder=placeholder, id="answer")

            yield Static("", id="status")
            yield OptionList(
                Option("▶  Verificar resposta", id="check"),
                Option("✎  Editar resposta (INSERT)", id="edit"),
                Option("←  Voltar", id="back"),
                id="task-actions",
            )

    def on_mount(self) -> None:
        super().on_mount()
        if hasattr(self.app, "set_nav_context"):
            self.app.set_nav_context(self.context_label)  # type: ignore[attr-defined]
        # NORMAL: nunca deixar o Input roubar o foco na abertura
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]
        try:
            self.query_one("#answer").blur()
        except Exception:
            pass
        self.call_after_refresh(self._enter_normal_focus)

    def _enter_normal_focus(self) -> None:
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]
        self.focus_nav_target()

    def enter_insert(self) -> None:
        try:
            field = self.query_one("#answer")
        except Exception:
            return
        field.focus()
        if hasattr(self.app, "enter_insert"):
            self.app.enter_insert()  # type: ignore[attr-defined]
        self.refresh_statusline()

    def action_vim_escape(self) -> None:
        if self.is_typing():
            self.set_focus(None)
            if hasattr(self.app, "enter_normal"):
                self.app.enter_normal()  # type: ignore[attr-defined]
            self.focus_nav_target()
            self.refresh_statusline()
            return
        self.action_vim_back()

    def _user_value(self) -> str:
        if self.quest.type == "code":
            return self.query_one("#answer", TextArea).text
        return self.query_one("#answer", Input).value

    def _check(self) -> None:
        status = self.query_one("#status", Static)
        ok, msg = validate_task(self.quest, self._user_value())
        if not ok:
            status.update(f"✗ {msg}")
            status.set_class(True, "err")
            status.set_class(False, "ok")
            return

        store = self.app.store  # type: ignore[attr-defined]
        result = store.mark_task(
            self.track.id,
            self.room.id,
            self.quest.id,
            self.quest.xp,
            self.room,
        )
        parts = [f"✓ {msg}"]
        if result["gained"]:
            parts.append(f"+{result['gained']} XP")
        parts.append(
            f"Total {result['xp']} XP · Nv {result['level']} · {result['rank'].title}"
        )
        if result["leveled"]:
            parts.append("LEVEL UP!")
        if result["ranked_up"]:
            parts.append(f"NOVO RANK: {result['rank'].title}")
        status.update("  ·  ".join(parts))
        status.set_class(True, "ok")
        status.set_class(False, "err")
        self.notify("  ·  ".join(parts), severity="information")
        if result.get("first_completion"):
            jr = journal_task_completion(
                track_id=self.track.id,
                room_id=self.room.id,
                task_id=self.quest.id,
                task_prompt=self.quest.prompt,
                xp_awarded=int(result.get("task_xp") or self.quest.xp),
            )
            if jr.warning:
                self.notify(jr.warning, severity="warning")
            elif jr.committed and jr.pushed:
                self.notify(f"GitHub · {jr.message}", severity="information")
            elif jr.committed:
                self.notify(f"Commit local · {jr.message}", severity="information")
        self.refresh_statusline()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        oid = str(event.option.id)
        if oid == "check":
            self._check()
        elif oid == "edit":
            self.enter_insert()
        elif oid == "back":
            self.app.pop_screen()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Enter no campo → verificar e voltar a NORMAL
        self._check()
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]
        self.set_focus(None)
        self.focus_nav_target()
