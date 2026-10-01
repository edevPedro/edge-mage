"""Resolver uma task — NORMAL/INSERT + victory juice."""

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
    pane_ids = ["prompt", "answer", "actions"]

    def __init__(
        self,
        track: Track,
        room: Room,
        quest: Task,
        *,
        mastery: bool = False,
        daily: bool = False,
        on_success=None,
    ) -> None:
        super().__init__()
        self.track = track
        self.room = room
        self.quest = quest
        self.mastery = mastery
        self.daily = daily
        self.on_success = on_success
        tag = "mastery" if mastery else ("daily" if daily else quest.id)
        self.context_label = f"{track.id}/{room.id}/{tag}"
        self.focused_pane = "actions"

    def compose_body(self) -> ComposeResult:
        store = self.app.store  # type: ignore[attr-defined]
        done = store.is_task_done(self.track.id, self.room.id, self.quest.id)
        mode = "MASTERY" if self.mastery else ("DAILY" if self.daily else self.quest.type.upper())
        with Vertical():
            yield Static(
                f"TASK · {mode} · +{self.quest.xp} XP",
                classes="title",
            )
            yield Static(
                "Ctrl+w painéis · i INSERT · Esc NORMAL",
                classes="muted",
            )
            with VerticalScroll(classes="panel", id="pane-prompt", can_focus=True):
                yield Static(self.quest.prompt)
                if self.quest.type == "mcq" and self.quest.choices:
                    lines = []
                    for i, c in enumerate(self.quest.choices):
                        letter = chr(ord("A") + i)
                        lines.append(f"  {letter}) {c}")
                    yield Static("\n".join(lines), classes="accent")
                if self.quest.hint:
                    yield Static(f"Dica: {self.quest.hint}", classes="muted")
                if self.quest.type == "ritual":
                    yield Static(
                        f"Artefato: study-log/artifacts/{self.quest.ritual_id or self.quest.id}.md",
                        classes="accent",
                    )
                if done and not self.mastery and not self.daily:
                    yield Static(
                        "✓ Já concluída — pode refazer sem XP (use M para mastery).",
                        classes="ok",
                    )

            if self.quest.type == "code":
                initial = self.quest.code_template or "# seu código aqui\n"
                yield TextArea(initial, id="answer")
            elif self.quest.type == "ritual":
                yield Input(
                    placeholder="digite ok após preencher o artefato",
                    id="answer",
                )
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
        user_val = self._user_value()
        if self.quest.type == "ritual":
            # qualquer input após arquivo válido
            ok, msg = validate_task(self.quest, user_val or "ok")
        else:
            ok, msg = validate_task(self.quest, user_val)
        if not ok:
            status.update(f"✗ {msg}")
            status.set_class(True, "err")
            status.set_class(False, "ok")
            return

        store = self.app.store  # type: ignore[attr-defined]

        if self.quest.type == "ritual":
            from edge_mage.rituals import complete_and_journal_ritual

            rid = self.quest.ritual_id or self.quest.id
            rok, rmsg = complete_and_journal_ritual(rid, store=store)
            if not rok:
                status.update(f"✗ {rmsg}")
                status.set_class(True, "err")
                return

        result = store.mark_task(
            self.track.id,
            self.room.id,
            self.quest.id,
            self.quest.xp,
            self.room,
            mastery=self.mastery,
        )

        # daily variant: mark as done in daily_run without needing real task id
        if self.daily and callable(self.on_success):
            self.on_success(result)

        skill_glyph = ""
        skill_name = ""
        newly_skills: list = []
        if result.get("room_completed"):
            newly_skills = self._grant_room_skills()
            if newly_skills:
                skill_glyph = newly_skills[0].glyph
                skill_name = newly_skills[0].name
            if self.room.elite_skill:
                elite = next(
                    (
                        s
                        for s in getattr(self.app, "skills", [])
                        if s.id == self.room.elite_skill
                    ),
                    None,
                )
                if elite:
                    skill_glyph = elite.glyph
                    skill_name = elite.name

        if result.get("first_completion") and not self.mastery and not self.daily:
            jr = journal_task_completion(
                track_id=self.track.id,
                room_id=self.room.id,
                task_id=self.quest.id,
                task_prompt=self.quest.prompt,
                xp_awarded=int(result.get("task_xp") or self.quest.xp),
            )
            if jr.warning:
                self.notify(jr.warning, severity="warning")

        status.update(f"✓ {msg}")
        status.set_class(True, "ok")
        status.set_class(False, "err")

        from edge_mage.screens.ceremony import CeremonyScreen

        title = "SALA CONCLUÍDA" if result.get("room_completed") else "ACERTO"
        if self.mastery:
            title = f"MASTERY {result.get('mastery', 0)}/3"
        if result.get("ranked_up"):
            title = "ASCENSÃO DE RANK"

        ceremony = CeremonyScreen(
            title=title,
            gained=int(result.get("gained") or 0),
            total_xp=int(result["xp"]),
            into=int(result.get("into_level") or 0),
            need=result.get("need_level"),
            level=int(result["level"]),
            leveled=bool(result.get("leveled")),
            rank_title=result["rank"].title,
            ranked_up=bool(result.get("ranked_up")),
            skill_glyph=skill_glyph,
            skill_name=skill_name,
            combo=int(result.get("combo") or 0),
            mult=float(result.get("mult") or 1.0),
            extra_lines=(
                [f"Mastery {result.get('mastery')}/3 — glyph shine"]
                if self.mastery and result.get("mastery")
                else []
            ),
        )
        # sai da task e mostra cerimônia por cima da sala
        self.app.pop_screen()
        self.app.push_screen(ceremony)

    def _grant_room_skills(self) -> list:
        from edge_mage.grimoire import skills_for_room

        app = self.app
        skills = getattr(app, "skills", []) or []
        granted = skills_for_room(
            skills, track_id=self.track.id, room_id=self.room.id
        )
        if not granted:
            return []
        store = app.store  # type: ignore[attr-defined]
        newly_ids = store.unlock_skills([s.id for s in granted])
        if newly_ids:
            store.save()
        return [s for s in granted if s.id in newly_ids]

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        oid = str(event.option.id)
        if oid == "check":
            self._check()
        elif oid == "edit":
            self.enter_insert()
        elif oid == "back":
            self.app.pop_screen()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._check()
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]
        self.set_focus(None)
        self.focus_nav_target()
