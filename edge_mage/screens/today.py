"""Tela HOJE — frontend diário da plataforma (§10), em blocos Wave.

Liga o motor do roadmap ao TUI: meta do dia, fonte de leitura, evidência,
streak, ramos e a curva da métrica. Ações: verificar, fechar o dia (explicação
de 3 linhas no campo inferior), ver gráfico (SVG via `wsh view`), abrir o work
dir e abrir a leitura.
"""

from __future__ import annotations

import shlex
from datetime import date

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from edge_mage import wave
from edge_mage.paths import charts_dir, practice_dir
from edge_mage.roadmap import branches as branches_mod
from edge_mage.roadmap import charts as charts_mod
from edge_mage.roadmap import daily as daily_mod
from edge_mage.roadmap import evidence as evidence_mod
from edge_mage.roadmap.errors import RoadmapError
from edge_mage.roadmap.loader import load_roadmap
from edge_mage.roadmap.runner import verify_goal
from edge_mage.screens.base import MageScreen
from edge_mage.widgets.wave import MetricStrip, SparklineBlock, WaveBlock


class TodayScreen(MageScreen):
    context_label = "hoje"
    list_id = "today-actions"
    pane_ids = ["hoje", "actions"]

    def __init__(self) -> None:
        super().__init__()
        self._roadmap = None
        self._state = None
        self._records: list = []
        self._ctx = None
        self._error = ""

    # -- carga -----------------------------------------------------------
    def _load(self) -> None:
        try:
            self._roadmap = load_roadmap()
        except RoadmapError as exc:
            self._error = str(exc)
            return
        self._state = daily_mod.load_state()
        self._records = evidence_mod.iter_all()
        self._ctx = daily_mod.today_context(self._roadmap, self._state, self._records)
        daily_mod.save_state(self._state)

    # -- composição ------------------------------------------------------
    def compose_body(self) -> ComposeResult:
        self._load()
        with Vertical(id="today-root"):
            yield Static("HOJE", classes="title")
            if self._error:
                yield WaveBlock("plataforma", [f"erro: {self._error}"])
                yield OptionList(Option("←  Voltar", id="back"), id="today-actions")
                return
            yield MetricStrip(id="today-metrics")
            yield WaveBlock(id="today-goal")
            yield SparklineBlock(id="today-spark")
            yield WaveBlock(id="today-branches")
            yield Static("explique o fechamento (3 partes separadas por ;):", classes="muted")
            yield Input(placeholder="o que medi; o que me surpreendeu; próximo passo", id="today-explain")
            yield OptionList(*self._options(), id="today-actions")

    def _options(self) -> list[Option]:
        if self._ctx is None:
            return [Option("←  Voltar", id="back")]
        return [
            Option("r  rodar verificação (mage verify)", id="verify"),
            Option("v  ver gráfico (SVG · wsh view)", id="chart"),
            Option("o  abrir work dir", id="workdir"),
            Option("l  abrir leitura (fonte)", id="source"),
            Option("↻  atualizar", id="refresh"),
            Option("←  Voltar", id="back"),
        ]

    def on_mount(self) -> None:
        super().on_mount()
        app = self.app
        if hasattr(app, "set_nav_context"):
            app.set_nav_context("hoje")  # type: ignore[attr-defined]
        self._refresh()

    # -- render ----------------------------------------------------------
    def _refresh(self) -> None:
        if self._error:
            return
        ctx = self._ctx
        streak = daily_mod.streak(self._records)
        passed = sum(1 for r in self._records if getattr(r, "is_pass", False))
        closed = sum(1 for e in (self._state.days or {}).values() if e.get("status") == "closed")

        self._metrics().set_metrics([
            ("streak", f"{streak}d"),
            ("evidências PASS", str(passed)),
            ("metas fechadas", str(closed)),
        ])
        self._goal_block().set_block("desafio ativo", self._goal_lines())
        self._branch_block().set_block("ramos", self._branch_lines())
        self._spark().set_series(*self._spark_data())

    def _metrics(self) -> MetricStrip:
        return self.query_one("#today-metrics", MetricStrip)

    def _goal_block(self) -> WaveBlock:
        return self.query_one("#today-goal", WaveBlock)

    def _branch_block(self) -> WaveBlock:
        return self.query_one("#today-branches", WaveBlock)

    def _spark(self) -> SparklineBlock:
        return self.query_one("#today-spark", SparklineBlock)

    def _goal_lines(self) -> list[str]:
        ctx = self._ctx
        if ctx is None:
            return ["tronco concluído ou vazio. (rode `mage roadmap`)"]
        ch = ctx.challenge
        lines = [
            f"{ch.id} — {ch.title}",
            f"meta [{ctx.goal.id}]: {ctx.goal.goal}",
        ]
        cmd = ch.verify_command(ctx.goal)
        if cmd:
            lines.append(f"verificar: {cmd}")
        wd = ch.resolved_work_dir(practice_dir())
        lines.append(f"work dir: {wd}{'' if wd.exists() else '  (rode `mage init`)'}")
        if ctx.source is not None:
            lines.append(f"leitura: {ctx.source.label()}")
        latest = evidence_mod.read_latest(ch.id)
        if latest is not None:
            head = "PASS" if latest.is_pass else latest.status
            lines.append(f"última evidência: [{head}] {latest.goal_id} · {latest.timestamp[:10]}")
        if ctx.needs_breakup:
            lines.append(f"AVISO: meta rolou {ctx.rollovers}x — quebre em passos menores.")
        return lines

    def _branch_lines(self) -> list[str]:
        lines: list[str] = []
        for st in branches_mod.statuses(self._roadmap, self._state):
            mark = "*" if st.active else ("o" if st.open else " ")
            state_txt = "ativo" if st.active else ("aberto" if st.open else st.reason)
            lines.append(f"{mark} {st.branch.id:20s} {state_txt}")
        warn = branches_mod.stagnation_warning(self._roadmap, self._state, self._records)
        if warn:
            lines.append(f"! {warn}")
        return lines or ["(nenhum)"]

    def _spark_data(self) -> tuple[str, list[float]]:
        ctx = self._ctx
        if ctx is None:
            return ("p99", [])
        pts = charts_mod.metric_series(self._records, challenge_id=ctx.challenge.id, stat="p99")
        pts = [(d, v) for d, v in pts if d]  # type: ignore[misc]
        return ("p99 (histórico)", [v for _, v in pts])

    # -- ações -----------------------------------------------------------
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        oid = str(event.option.id)
        if oid == "back":
            self.app.pop_screen()
        elif oid == "verify":
            self._do_verify()
        elif oid == "chart":
            self._do_chart()
        elif oid == "workdir":
            self._do_workdir()
        elif oid == "source":
            self._do_source()
        elif oid == "refresh":
            self._reload()

    def _reload(self) -> None:
        self._load()
        try:
            lst = self.query_one("#today-actions", OptionList)
            lst.clear_options()
            lst.add_options(self._options())
        except Exception:
            return
        self._refresh()

    def _notice(self, msg: str, *, severity: str = "information") -> None:
        self.app.notify(msg, severity=severity)

    def _do_verify(self) -> None:
        ctx = self._ctx
        if ctx is None:
            return
        self._notice(f"verificando {ctx.goal.id}… rode com calma.")
        self._run_verify(ctx.challenge.id, ctx.goal.id)

    @work(thread=True)
    def _run_verify(self, challenge_id: str, goal_id: str) -> None:
        ctx = self._ctx
        if ctx is None:
            return
        wd = ctx.challenge.resolved_work_dir(practice_dir())
        run = verify_goal(ctx.challenge, ctx.challenge.goal(goal_id), wd)
        head = "PASS" if run.outcome.ok else run.outcome.status
        self.app.call_from_thread(
            self._notice,
            f"[{head}] {run.outcome.stage} · {run.outcome.message}",
            severity="information" if run.outcome.ok else "warning",
        )
        self.app.call_from_thread(self._reload)

    def _do_chart(self) -> None:
        ctx = self._ctx
        if ctx is None:
            return
        pts = charts_mod.metric_series(self._records, challenge_id=ctx.challenge.id, stat="p99")
        title = f"{ctx.challenge.id} · p99 (n={len(pts)})"
        svg = charts_mod.line_chart_svg(pts, title=title)  # type: ignore[arg-type]
        out = charts_mod.write_svg(charts_dir() / f"curve-{ctx.challenge.id}.svg", svg)
        res = wave.view(out)
        self._notice(res.message or f"chart: {out}")

    def _do_workdir(self) -> None:
        ctx = self._ctx
        if ctx is None:
            return
        wd = ctx.challenge.resolved_work_dir(practice_dir())
        if not wd.exists():
            self._notice(f"work dir não existe — rode `mage init {ctx.challenge.id}`", severity="warning")
            return
        res = wave.run(["bash", "-lc", f"cd {shlex.quote(str(wd))} && pwd && ls -la"])
        self._notice(res.message or f"work dir: {wd}")

    def _do_source(self) -> None:
        ctx = self._ctx
        if ctx is None:
            return
        if ctx.source is not None and ctx.source.url:
            res = wave.open_url(ctx.source.url)
            self._notice(res.message or f"abrindo {ctx.source.url}")
        elif ctx.source is not None:
            self._notice(f"leitura: {ctx.source.label()}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id != "today-explain":
            return
        explanation = event.value.strip()
        event.input.value = ""
        if self._ctx is None:
            return
        parts = [p for p in explanation.replace("\\n", "\n").split(";") if p.strip()]
        if len(parts) < 3 and len([ln for ln in explanation.splitlines() if ln.strip()]) < 3:
            self._notice("a explicação precisa de 3 partes (o que medi; surpreendeu; próximo).", severity="warning")
            return
        latest = evidence_mod.read_latest(self._ctx.challenge.id)
        if latest is None or latest.goal_id != self._ctx.goal.id or not latest.is_pass:
            self._notice("sem evidência PASS para a meta de hoje — rode a verificação primeiro.", severity="warning")
            return
        path = evidence_mod.attach_explanation(self._ctx.challenge.id, self._ctx.goal.id, explanation)
        daily_mod.close_day(
            self._state,
            challenge_id=self._ctx.challenge.id,
            goal_id=self._ctx.goal.id,
            explanation=explanation,
            evidence_path=str(path) if path else "",
        )
        daily_mod.save_state(self._state)
        self._notice(f"dia fechado · meta {self._ctx.goal.id} concluída")
        self._reload()

    def open_default(self) -> None:
        lst = self._option_list()
        if lst is not None:
            lst.action_select()
