"""App Textual principal do Edge Mage."""

from __future__ import annotations

from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Input, TextArea

from edge_mage.commands import parse_command
from edge_mage.content import find_room, load_all_tracks
from edge_mage.git_journal import sync_study_journal
from edge_mage.grimoire import load_skills
from edge_mage.models import Track
from edge_mage.nav import NavMode
from edge_mage.progress import ProgressStore
from edge_mage.screens.base import MageScreen
from edge_mage.screens.home import HomeScreen
from edge_mage.theme import THEME_CSS
from edge_mage.widgets.cmdline import CmdlineScreen


class EdgeMageApp(App[None]):
    TITLE = "Edge Mage"
    SUB_TITLE = "Academia · Math → Edge AI"
    CSS = THEME_CSS
    BINDINGS = [
        Binding("j", "vim_down", show=False, priority=True),
        Binding("k", "vim_up", show=False, priority=True),
        Binding("h", "vim_back", show=False, priority=True),
        Binding("l", "vim_open", show=False, priority=True),
        Binding("enter", "vim_open", show=False, priority=True),
        Binding("G", "vim_bottom", show=False, priority=True),
        Binding("space", "vim_anim", show=False, priority=True),
        Binding("i", "vim_insert", show=False, priority=True),
        Binding("q", "smart_quit", show=False, priority=True),
        Binding("question_mark", "show_help", show=False, priority=True),
        Binding("colon", "open_cmdline", show=False, priority=True),
        Binding("ctrl+w", "window_prefix", show=False, priority=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.store = ProgressStore()
        self.tracks: list[Track] = load_all_tracks()
        self.skills = load_skills()
        self.skills_total = len(self.skills)
        self.nav_mode: NavMode = NavMode.NORMAL
        self.nav_context: str = "home"
        self._leader: str | None = None

    def on_mount(self) -> None:
        self.store.touch_streak()
        self._backfill_skills()
        self.push_screen(HomeScreen())

    def _backfill_skills(self) -> None:
        """Desbloqueia skills de salas já concluídas (progresso antigo)."""
        from edge_mage.grimoire import skills_for_room

        newly_all: list[str] = []
        for track in self.tracks:
            for room in track.rooms:
                if not self.store.is_room_done(track.id, room.id):
                    continue
                granted = skills_for_room(
                    self.skills, track_id=track.id, room_id=room.id
                )
                newly_all.extend(
                    self.store.unlock_skills([s.id for s in granted])
                )
        if newly_all:
            self.store.save()

    def compose(self) -> ComposeResult:
        return
        yield  # pragma: no cover

    def _focused_is_input(self) -> bool:
        return isinstance(self.focused, (Input, TextArea))

    def _in_insert(self) -> bool:
        return self.nav_mode == NavMode.INSERT or (
            self.nav_mode != NavMode.COMMAND and self._focused_is_input()
        )

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if action == "window_prefix":
            if self.nav_mode == NavMode.COMMAND or self._in_insert():
                return False
            return True
        if action in {
            "vim_down",
            "vim_up",
            "vim_back",
            "vim_open",
            "vim_bottom",
            "vim_anim",
            "vim_insert",
            "smart_quit",
            "show_help",
            "open_cmdline",
        }:
            if self.nav_mode == NavMode.COMMAND:
                return False
            if self.nav_mode == NavMode.WINDOW:
                # teclas h/j/k/l/w tratadas em on_key
                return False
            if self._in_insert():
                return False
            if self._leader == "g" and action != "smart_quit":
                return False
        return True

    def set_nav_mode(self, mode: NavMode | str) -> None:
        if isinstance(mode, str):
            try:
                mode = NavMode(mode)
            except ValueError:
                mode = NavMode.NORMAL
        self.nav_mode = mode
        screen = self.screen
        if isinstance(screen, MageScreen):
            screen.refresh_statusline()

    def enter_normal(self) -> None:
        self._leader = None
        self.set_nav_mode(NavMode.NORMAL)

    def enter_insert(self) -> None:
        self._leader = None
        self.set_nav_mode(NavMode.INSERT)

    def enter_window(self) -> None:
        self._leader = None
        self.set_nav_mode(NavMode.WINDOW)

    def set_nav_context(self, context: str) -> None:
        self.nav_context = context
        screen = self.screen
        if isinstance(screen, MageScreen):
            screen.context_label = context
            screen.refresh_statusline()

    def _mage(self) -> MageScreen | None:
        screen = self.screen
        return screen if isinstance(screen, MageScreen) else None

    def action_window_prefix(self) -> None:
        """Ctrl+w: entra em modo janela (nvim). 2º w / Ctrl+w cicla."""
        if self._in_insert() or self.nav_mode == NavMode.COMMAND:
            return
        if self.nav_mode == NavMode.WINDOW:
            m = self._mage()
            if m and m.pane_ids:
                m.cycle_pane(1)
            self.enter_normal()
            return
        m = self._mage()
        if not m or not m.pane_ids:
            self.notify("sem painéis nesta tela", severity="information")
            return
        self.enter_window()

    def action_vim_down(self) -> None:
        m = self._mage()
        if m:
            m.action_vim_down()
            # não re-focar OptionList se estamos num scroll pane
            if m.focused_pane in {None, "tasks", "actions"} or not m.pane_ids:
                m.focus_nav_target()

    def action_vim_up(self) -> None:
        m = self._mage()
        if m:
            m.action_vim_up()
            if m.focused_pane in {None, "tasks", "actions"} or not m.pane_ids:
                m.focus_nav_target()

    def action_vim_back(self) -> None:
        m = self._mage()
        if m:
            m.action_vim_back()

    def action_vim_open(self) -> None:
        m = self._mage()
        if m:
            m.action_vim_open()

    def action_vim_bottom(self) -> None:
        m = self._mage()
        if m:
            m.action_vim_bottom()
            m.focus_nav_target()

    def action_vim_anim(self) -> None:
        m = self._mage()
        if m:
            m.action_vim_anim()

    def action_vim_insert(self) -> None:
        m = self._mage()
        if m:
            m.action_vim_insert()

    def on_key(self, event: events.Key) -> None:
        if self.nav_mode == NavMode.COMMAND:
            return

        if self.nav_mode == NavMode.WINDOW:
            event.stop()
            event.prevent_default()
            key = event.character or event.key
            m = self._mage()
            if event.key == "escape":
                self.enter_normal()
                return
            if key in {"w", "W"} or event.key == "ctrl+w":
                if m and m.pane_ids:
                    m.cycle_pane(1)
                self.enter_normal()
                return
            if key in {"h", "j", "k", "l"}:
                if m and m.pane_ids:
                    m.move_pane(key)
                self.enter_normal()
                return
            # tecla inválida: cancela modo janela
            self.enter_normal()
            return

        if self._in_insert():
            if self.nav_mode != NavMode.INSERT and self._focused_is_input():
                self.set_nav_mode(NavMode.INSERT)
            return

        if self._leader == "g":
            event.stop()
            event.prevent_default()
            if event.key == "escape":
                self._leader = None
                self.enter_normal()
                return
            self._leader = None
            self.enter_normal()
            key = event.character or event.key
            if key == "g":
                m = self._mage()
                if m:
                    m.action_vim_top()
                    m.focus_nav_target()
            elif key == "p":
                self.action_go_profile()
            elif key == "t":
                self.action_go_tracks()
            elif key == "h":
                self.action_go_home()
            elif key == "r":
                self.action_go_grimoire()
            return

        if event.character == "g":
            event.stop()
            event.prevent_default()
            self._leader = "g"
            self.set_nav_mode(NavMode.LEADER)
            return

    def action_smart_quit(self) -> None:
        if self._in_insert() or self.nav_mode == NavMode.COMMAND:
            return
        self.exit()

    def action_open_cmdline(self) -> None:
        if self._in_insert():
            return
        self._leader = None
        self.set_nav_mode(NavMode.COMMAND)

        def _done(result: str | None) -> None:
            self.enter_normal()
            if result:
                self.dispatch_colon(result)

        self.push_screen(CmdlineScreen(), _done)

    def action_show_help(self) -> None:
        if self._in_insert():
            return
        from edge_mage.screens.help import HelpScreen

        self.push_screen(HelpScreen())

    def action_go_home(self) -> None:
        self.push_screen(HomeScreen())

    def action_go_profile(self) -> None:
        from edge_mage.screens.profile import ProfileScreen

        self.push_screen(ProfileScreen())

    def action_go_grimoire(self) -> None:
        from edge_mage.screens.grimoire import GrimoireScreen

        self.push_screen(GrimoireScreen())

    def action_go_tracks(self) -> None:
        from edge_mage.screens.tracks import TracksScreen

        self.push_screen(TracksScreen())

    def dispatch_colon(self, line: str) -> None:
        cmd = parse_command(line)
        if cmd.error:
            self.notify(cmd.error, severity="warning")
            return
        if cmd.name == "quit":
            self.exit()
        elif cmd.name == "tracks":
            self.action_go_tracks()
        elif cmd.name == "profile":
            self.action_go_profile()
        elif cmd.name == "grimoire":
            self.action_go_grimoire()
        elif cmd.name == "home":
            self.action_go_home()
        elif cmd.name == "help":
            self.action_show_help()
        elif cmd.name == "anim":
            screen = self.screen
            toggle = getattr(screen, "toggle_animation", None)
            if callable(toggle):
                kind = cmd.args[0] if cmd.args else None
                toggle(kind)
            else:
                self.notify("animação só em salas com visual", severity="warning")
        elif cmd.name == "xp":
            p = self.store.profile_summary()
            nxt = p["next_rank"]
            extra = f" → {nxt.title} ({nxt.min_xp})" if nxt else " (rank máx.)"
            skills = f" · grimório {p.get('skills_done', 0)}/{self.skills_total}"
            self.notify(
                f"XP {p['xp']} · Nv {p['level']} · {p['rank'].title}{extra}{skills}",
                severity="information",
            )
        elif cmd.name == "sync":
            jr = sync_study_journal()
            if jr.warning:
                self.notify(jr.warning, severity="warning")
            elif jr.pushed:
                self.notify("Diário sincronizado com origin", severity="information")
            elif jr.message:
                self.notify(jr.message, severity="information")
            else:
                self.notify("Nada a sincronizar", severity="information")
        elif cmd.name == "room":
            room_id = cmd.args[0]
            found = None
            for track in self.tracks:
                room = find_room(track, room_id)
                if room is not None:
                    found = (track, room)
                    break
            if found is None:
                matches = [
                    (t, r)
                    for t in self.tracks
                    for r in t.rooms
                    if room_id in r.id or room_id.lower() in r.title.lower()
                ]
                if len(matches) == 1:
                    found = matches[0]
                elif len(matches) > 1:
                    ids = ", ".join(r.id for _, r in matches[:6])
                    self.notify(f"várias salas: {ids}", severity="warning")
                    return
            if found is None:
                self.notify(f"sala não encontrada: {room_id}", severity="error")
                return
            track, room = found
            if not self.store.is_room_unlocked(track, room):
                self.notify(
                    f"sala bloqueada — precisa de {room.unlock_xp} XP",
                    severity="warning",
                )
                return
            from edge_mage.screens.room import RoomScreen

            self.push_screen(RoomScreen(track, room))


def run() -> None:
    EdgeMageApp().run()
