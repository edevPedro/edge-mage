"""Daily Run — review + new task do dia."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from edge_mage.content import find_room, find_track
from edge_mage.daily import build_daily_run, daily_task_from_payload
from edge_mage.models import Room
from edge_mage.screens.base import MageScreen


class DailyRunScreen(MageScreen):
    context_label = "daily"
    list_id = "daily-actions"

    def compose_body(self) -> ComposeResult:
        app = self.app
        store = app.store  # type: ignore[attr-defined]
        tracks = app.tracks  # type: ignore[attr-defined]
        data = build_daily_run(store, tracks)
        rev = data.get("review")
        new = data.get("new")
        lines = [
            f"Data: {data.get('date')}",
            f"Passo: {int(data.get('review_done', False)) + int(data.get('new_done', False))}/2",
            "",
            "1) Review — sala limpa (variante do dia)",
            f"   {'✓' if data.get('review_done') else '○'}  "
            + (
                (rev.get("prompt", "")[:64] + ("…" if rev and len(rev.get("prompt", "")) > 64 else ""))
                if rev
                else "(complete uma sala para habilitar review)"
            ),
            "",
            "2) Nova — próxima porta pedagógica",
            f"   {'✓' if data.get('new_done') else '○'}  "
            + (
                f"{new.get('track_id')}/{new.get('room_id')}/{new.get('task_id')}"
                if new
                else "(currículo completo)"
            ),
            "",
            "~20 min · seed fixa pela data · Ctrl+w nos painéis da task",
        ]
        with Vertical():
            yield Static("RUN DE HOJE", classes="title")
            yield Static("\n".join(lines), classes="panel")
            opts: list[Option] = []
            if rev and not data.get("review_done"):
                opts.append(Option("▶  Fazer review", id="review"))
            if new and not data.get("new_done"):
                opts.append(Option("▶  Fazer task nova", id="new"))
            if data.get("review_done") and data.get("new_done"):
                opts.append(Option("✧  Run completa", id="done"))
            opts.append(Option("←  Voltar", id="back"))
            yield OptionList(*opts, id="daily-actions")

    def on_mount(self) -> None:
        super().on_mount()
        if hasattr(self.app, "set_nav_context"):
            self.app.set_nav_context("daily")  # type: ignore[attr-defined]
        if hasattr(self.app, "enter_normal"):
            self.app.enter_normal()  # type: ignore[attr-defined]

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        oid = str(event.option.id)
        if oid == "back":
            self.app.pop_screen()
            return
        store = self.app.store  # type: ignore[attr-defined]
        tracks = self.app.tracks  # type: ignore[attr-defined]
        data = build_daily_run(store, tracks)
        if oid == "done":
            from edge_mage.screens.ceremony import CeremonyScreen

            course = getattr(self.app, "course", None) or ""
            p = store.profile_summary(course if course else None)
            self.app.push_screen(
                CeremonyScreen(
                    title="RUN DO DIA COMPLETA",
                    gained=0,
                    total_xp=p["xp"],
                    into=p["into_level"],
                    need=p["need_level"],
                    level=p["level"],
                    rank_title=p["rank"].title,
                    combo=int(p.get("combo") or 0),
                    mult=float(p.get("mult") or 1.0),
                    extra_lines=["Volte amanhã — novo seed."],
                )
            )
            return
        if oid == "review" and data.get("review"):
            self._start_review(data)
        elif oid == "new" and data.get("new"):
            self._start_new(data)

    def _reload(self) -> None:
        self.app.pop_screen()
        self.app.push_screen(DailyRunScreen())

    def _start_review(self, data: dict) -> None:
        from edge_mage.screens.task import TaskScreen

        payload = data["review"]
        tracks = self.app.tracks  # type: ignore[attr-defined]
        track = find_track(tracks, payload["track_id"])
        if track is None:
            return
        room = find_room(track, payload["room_id"]) or Room(
            id=payload["room_id"],
            title=payload["room_id"],
            summary="",
            xp_reward=0,
            unlock_xp=0,
            lesson_md="",
            tasks=[],
            path="",
        )
        task = daily_task_from_payload(payload)
        store = self.app.store  # type: ignore[attr-defined]

        def _ok(_result=None) -> None:
            d = store.get_daily_run()
            d["review_done"] = True
            d["step"] = max(int(d.get("step") or 0), 1)
            store.set_daily_run(d)

        def _after_task(_r=None) -> None:
            self._reload()

        # TaskScreen pops itself after ceremony; we reload daily on resume via wrapping
        screen = TaskScreen(
            track, room, task, daily=True, mastery=True, on_success=_ok
        )
        self.app.push_screen(screen)

    def _start_new(self, data: dict) -> None:
        from edge_mage.screens.task import TaskScreen

        payload = data["new"]
        tracks = self.app.tracks  # type: ignore[attr-defined]
        track = find_track(tracks, payload["track_id"])
        room = find_room(track, payload["room_id"]) if track else None
        if not track or not room:
            return
        task = next((t for t in room.tasks if t.id == payload["task_id"]), room.tasks[0])
        store = self.app.store  # type: ignore[attr-defined]

        def _ok(_result=None) -> None:
            d = store.get_daily_run()
            d["new_done"] = True
            d["step"] = 2
            store.set_daily_run(d)

        self.app.push_screen(
            TaskScreen(track, room, task, daily=True, on_success=_ok)
        )

    def on_screen_resume(self) -> None:
        super().on_screen_resume()
        # atualiza texto/opções sem re-empilhar
        try:
            lst = self.query_one("#daily-actions", OptionList)
        except Exception:
            return
        store = self.app.store  # type: ignore[attr-defined]
        tracks = self.app.tracks  # type: ignore[attr-defined]
        data = build_daily_run(store, tracks)
        opts: list[Option] = []
        if data.get("review") and not data.get("review_done"):
            opts.append(Option("▶  Fazer review", id="review"))
        if data.get("new") and not data.get("new_done"):
            opts.append(Option("▶  Fazer task nova", id="new"))
        if data.get("review_done") and data.get("new_done"):
            opts.append(Option("✧  Run completa", id="done"))
        opts.append(Option("←  Voltar", id="back"))
        lst.clear_options()
        lst.add_options(opts)
