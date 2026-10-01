"""App Textual principal do Edge Mage."""

from __future__ import annotations

from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Input, TextArea

from edge_mage.commands import parse_command
from edge_mage.content import find_room, load_all_tracks
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
    # priority=True: teclas chegam mesmo com OptionList/Button focado.
    # check_action desliga em INSERT para não roubar digitação.
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
    ]

    def __init__(self) -> None:
        super().__init__()
        self.store = ProgressStore()
        self.tracks: list[Track] = load_all_tracks()
        self.nav_mode: NavMode = NavMode.NORMAL
        self.nav_context: str = "home"
        self._leader: str | None = None

    def on_mount(self) -> None:
        self.store.touch_streak()
        self.push_screen(HomeScreen())

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
        """Em INSERT/COMMAND, libera teclas alfanuméricas para o Input."""
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
            if self._in_insert():
                return False
            if self._leader == "g" and action != "smart_quit":
                # leader consome via on_key
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

    def set_nav_context(self, context: str) -> None:
        self.nav_context = context
        screen = self.screen
        if isinstance(screen, MageScreen):
            screen.context_label = context
            screen.refresh_statusline()

    def _mage(self) -> MageScreen | None:
        screen = self.screen
        return screen if isinstance(screen, MageScreen) else None

    def action_vim_down(self) -> None:
        m = self._mage()
        if m:
            m.action_vim_down()
            m.focus_nav_target()

    def action_vim_up(self) -> None:
        m = self._mage()
        if m:
            m.action_vim_up()
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

        if self._in_insert():
            if self.nav_mode != NavMode.INSERT and self._focused_is_input():
                self.set_nav_mode(NavMode.INSERT)
            return

        # Leader g + 2ª tecla
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
            self.notify(
                f"XP {p['xp']} · Nv {p['level']} · {p['rank'].title}{extra}",
                severity="information",
            )
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
