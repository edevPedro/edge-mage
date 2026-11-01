"""CLI da plataforma diária: mage today / verify / close / week / roadmap."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from edge_mage.paths import charts_dir, practice_dir
from edge_mage.roadmap import branches as branches_mod
from edge_mage.roadmap import charts as charts_mod
from edge_mage.roadmap import daily as daily_mod
from edge_mage.roadmap import evidence as evidence_mod
from edge_mage.roadmap.errors import RoadmapError
from edge_mage.roadmap.loader import load_roadmap
from edge_mage.roadmap.models import Challenge, DailyGoal
from edge_mage.roadmap.runner import format_outcome, verify_goal

_USAGE = """uso: mage <comando>

  roadmap            visão do tronco (desafios, metas, ramos)
  today              meta de hoje (menor passo com verificador) + fonte
  verify [--runs N]  roda o verificador da meta de hoje e grava evidência
  close --explain "l1; l2; l3"
                     fecha o dia (explicação de 3 linhas obrigatória)
  week [--svg]       painel semanal (horas, metas, evidência, dispersão)
  branch <id>        ativa um ramo (--off <id> desativa; sem args, lista)
  chart [--challenge <id>] [--metric <m>] [--stat p99]
                     gera SVG da curva da métrica no tempo (~/.mage/charts/)
  init [<challenge>] cria o diretório de trabalho a partir do scaffold
  workdir [<challenge>]
                     imprime o work dir do desafio ativo (cria se faltar)
"""


def _records():
    return evidence_mod.iter_all()


def _load():
    roadmap = load_roadmap()
    state = daily_mod.load_state()
    records = _records()
    return roadmap, state, records


def _fmt_date(ts: str) -> str:
    return ts.split("T", 1)[0] if ts else "—"


def cmd_roadmap(argv: list[str]) -> int:
    try:
        roadmap, state, records = _load()
    except RoadmapError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    print(f"e-mage · tronco {roadmap.trunk_track} · meta diária {roadmap.daily_minutes} min")
    print(f"daily_minutes={roadmap.daily_minutes} · ramos≤{roadmap.rules.branches_max_pct:.0f}% "
          f"tronco≥{roadmap.rules.trunk_min_pct:.0f}% · máx {roadmap.rules.max_active_branches} ramos\n")
    active = state.active_challenge
    for ch in roadmap.trunk_challenges():
        done = daily_mod.done_goals(state, ch.id)
        total = len(ch.daily_goals)
        mark = "*" if ch.id == active else " "
        status = "concluído" if total and len(done) >= total else f"{len(done)}/{total} metas"
        print(f"{mark} {ch.id:18s} [{ch.track}] {ch.title}")
        print(f"    {status} · timebox {ch.timebox_days}d · {ch.dir.name}")
    if roadmap.branches:
        print("\nramos (abrem por evidência ou calendário):")
        for st in branches_mod.statuses(roadmap, state):
            b = st.branch
            mark = "*" if st.active else ("o" if st.open else " ")
            state_txt = "ativo" if st.active else ("aberto" if st.open else st.reason)
            print(f"{mark} {b.id:22s} {state_txt:30s} teto {b.weekly_cap_pct:.0f}%")
            if st.active and b.title:
                print(f"    {b.title}")
    warn = branches_mod.stagnation_warning(roadmap, state, records)
    if warn:
        print(f"\n! {warn}")
    pct, _tn, tot = branches_mod.trunk_share(records, roadmap)
    if tot and pct < roadmap.rules.trunk_min_pct:
        print(f"! tronco em {pct:.0f}% (< {roadmap.rules.trunk_min_pct:.0f}%) na última semana — "
              f"mantenha ramos ≤ {roadmap.rules.branches_max_pct:.0f}% (§3)")
    return 0


def cmd_today(argv: list[str]) -> int:
    try:
        roadmap, state, records = _load()
    except RoadmapError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    ctx = daily_mod.today_context(roadmap, state, records)
    st = daily_mod.streak(records)
    if ctx is None:
        print("tronco concluído ou vazio. Nada a fazer hoje. (rode `mage roadmap`)")
        print(f"streak: {st} dia(s)")
        daily_mod.save_state(state)
        return 0
    line = "─" * 60
    print(line)
    print(f"HOJE · {date.today().isoformat()} · streak {st} dia(s)")
    print(line)
    print(f"desafio ativo: {ctx.challenge.id} — {ctx.challenge.title}")
    if ctx.challenge.exit_criteria.metric:
        print(f"critério de saída: {ctx.challenge.exit_criteria.metric} "
              f"{ctx.challenge.exit_criteria.target}")
    print()
    if ctx.source is not None:
        print("leitura (~15%):")
        print(f"  {ctx.source.label()}")
        if ctx.source.url:
            print(f"  {ctx.source.url}")
        if ctx.source.why:
            print(f"  por quê: {ctx.source.why}")
        print()
    print("lab (~70%) — meta do dia:")
    print(f"  → [{ctx.goal.id}] {ctx.goal.goal}")
    cmd = ctx.challenge.verify_command(ctx.goal)
    if cmd:
        print(f"  verificar com: {cmd}")
    wd = ctx.challenge.resolved_work_dir(practice_dir())
    print(f"  work dir: {wd}{'' if wd.exists() else '  (rode `mage init` para criar)'}")
    print()
    if ctx.needs_breakup:
        print(f"AVISO: esta meta já rolou {ctx.rollovers}x. Quebre em passos menores:")
        print("  divida em 2-3 metas com verificadores próprios antes de continuar.")
        print()
    latest = evidence_mod.read_latest(ctx.challenge.id)
    if latest is not None:
        head = "PASS" if latest.is_pass else latest.status
        print(f"última evidência: [{head}] {ctx.goal.id if latest.goal_id==ctx.goal.id else latest.goal_id} "
              f"· {_fmt_date(latest.timestamp)}")
    else:
        print("última evidência: (nenhuma)")
    print()
    print("fechamento (~15%): rode `mage verify` e depois `mage close` com 3 linhas.")
    daily_mod.save_state(state)
    return 0


def _resolve_goal(ctx: daily_mod.GoalContext, goal_id: str, records: list) -> DailyGoal | None:
    if not goal_id:
        return ctx.goal
    return ctx.challenge.goal(goal_id)


def cmd_verify(argv: list[str]) -> int:
    runs = None
    goal_id = ""
    rest = list(argv)
    while rest:
        tok = rest.pop(0)
        if tok == "--runs" and rest:
            try:
                runs = int(rest.pop(0))
            except ValueError:
                print("--runs espera um inteiro", file=sys.stderr)
                return 2
        elif tok.startswith("--runs="):
            try:
                runs = int(tok.split("=", 1)[1])
            except ValueError:
                print("--runs espera um inteiro", file=sys.stderr)
                return 2
        elif tok == "--goal" and rest:
            goal_id = rest.pop(0)
        elif tok.startswith("--goal="):
            goal_id = tok.split("=", 1)[1]
        else:
            print(f"argumento desconhecido: {tok}", file=sys.stderr)
            return 2
    try:
        roadmap, state, records = _load()
    except RoadmapError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    ctx = daily_mod.today_context(roadmap, state, records)
    if ctx is None:
        print("nenhuma meta ativa para verificar.", file=sys.stderr)
        return 1
    goal = _resolve_goal(ctx, goal_id, records)
    if goal is None:
        print(f"meta '{goal_id}' não existe em {ctx.challenge.id}", file=sys.stderr)
        return 2
    wd = ctx.challenge.resolved_work_dir(practice_dir())
    run = verify_goal(ctx.challenge, goal, wd, runs=runs)
    print(format_outcome(run.outcome, record=run.record))
    print(f"\nevidence: {run.evidence_path}")
    daily_mod.save_state(state)
    if run.outcome.ok:
        print("\nPASS — feche o dia: mage close --explain \"o que medi; o que me surpreendeu; próximo passo\"")
    return 0 if run.outcome.ok else 1


def _parse_explain(rest: list[str]) -> str | None:
    for i, tok in enumerate(rest):
        if tok == "--explain" and i + 1 < len(rest):
            return rest[i + 1]
        if tok.startswith("--explain="):
            return tok.split("=", 1)[1]
    return None


def cmd_close(argv: list[str]) -> int:
    explanation = _parse_explain(list(argv))
    if not explanation:
        print("explicação obrigatória (3 linhas):", file=sys.stderr)
        print('  mage close --explain "o que medi; o que me surpreendeu; próximo passo"', file=sys.stderr)
        return 2
    lines = [ln for ln in explanation.replace("\\n", "\n").split(";") if ln.strip()]
    if len(lines) < 3 and len([ln for ln in explanation.splitlines() if ln.strip()]) < 3:
        print("a explicação precisa de 3 partes (o que medi; o que me surpreendeu; próximo passo).",
              file=sys.stderr)
        return 2
    try:
        roadmap, state, records = _load()
    except RoadmapError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    ctx = daily_mod.today_context(roadmap, state, records)
    if ctx is None:
        print("nenhuma meta ativa.", file=sys.stderr)
        return 1
    latest = evidence_mod.read_latest(ctx.challenge.id)
    if latest is None or latest.goal_id != ctx.goal.id or not latest.is_pass:
        print("sem evidência PASS para a meta de hoje — rode `mage verify` primeiro.", file=sys.stderr)
        return 1
    path = evidence_mod.attach_explanation(ctx.challenge.id, ctx.goal.id, explanation.strip())
    entry = daily_mod.close_day(
        state,
        challenge_id=ctx.challenge.id,
        goal_id=ctx.goal.id,
        explanation=explanation.strip(),
        evidence_path=str(path) if path else "",
    )
    daily_mod.save_state(state)
    print(f"dia fechado · meta {ctx.goal.id} concluída · streak {daily_mod.streak(_records())} dia(s)")
    print(f"explanation gravada em {path}")
    return 0


def cmd_init(argv: list[str]) -> int:
    import shutil

    try:
        roadmap, state, records = _load()
    except RoadmapError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    cid = argv[0] if argv else state.active_challenge
    if not cid:
        ctx = daily_mod.today_context(roadmap, state, records)
        cid = ctx.challenge.id if ctx else ""
    ch: Challenge | None = roadmap.challenge(cid)
    if ch is None:
        print(f"desafio '{cid}' não encontrado no roadmap.", file=sys.stderr)
        return 2
    state.active_challenge = ch.id
    if not state.started_at:
        from datetime import datetime, timezone

        state.started_at = datetime.now(timezone.utc).isoformat()
    daily_mod.save_state(state)
    work = ch.resolved_work_dir(practice_dir())
    scaffold = ch.scaffold_dir()
    work.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    if scaffold.exists():
        for item in sorted(scaffold.rglob("*")):
            if not item.is_file():
                continue
            rel = item.relative_to(scaffold)
            dest = work / rel
            if dest.exists() and "--force" not in argv:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)
            copied.append(rel.as_posix())
    print(f"work dir: {work}")
    if copied:
        print("arquivos criados: " + ", ".join(copied))
    elif scaffold.exists():
        print("nada novo (use --force para sobrescrever)")
    else:
        print("sem scaffold — crie seus arquivos no work dir.")
    return 0


def cmd_workdir(argv: list[str]) -> int:
    """Printa o work dir do desafio ativo (cria se faltar). Útil p/ widgets e scripting."""
    try:
        roadmap, state, records = _load()
    except RoadmapError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    cid = argv[0] if argv else state.active_challenge
    if not cid:
        ctx = daily_mod.today_context(roadmap, state, records)
        cid = ctx.challenge.id if ctx else ""
    ch: Challenge | None = roadmap.challenge(cid) if cid else None
    if ch is None:
        print("nenhum desafio ativo — rode `mage init <desafio>`.", file=sys.stderr)
        return 2
    wd = ch.resolved_work_dir(practice_dir())
    wd.mkdir(parents=True, exist_ok=True)
    print(wd)
    return 0


def cmd_branch(argv: list[str]) -> int:
    try:
        roadmap, state, records = _load()
    except RoadmapError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    action = "on"
    ids: list[str] = []
    for tok in argv:
        if tok in ("--off", "off"):
            action = "off"
        elif tok in ("--on", "on"):
            action = "on"
        elif tok.startswith("-"):
            print(f"argumento desconhecido: {tok}", file=sys.stderr)
            return 2
        else:
            ids.append(tok)
    if not ids:
        print("ramos (o=aberto, *=ativo):")
        for st in branches_mod.statuses(roadmap, state):
            mark = "*" if st.active else ("o" if st.open else " ")
            state_txt = "ativo" if st.active else ("aberto" if st.open else st.reason)
            print(f"  {mark} {st.branch.id:22s} {state_txt}")
        return 0
    for bid in ids:
        if action == "off":
            ok = branches_mod.deactivate(state, bid)
            print(f"ramo '{bid}' desativado" if ok else f"ramo '{bid}' não estava ativo")
        else:
            ok, msg = branches_mod.activate(roadmap, state, bid)
            print(msg)
            if not ok:
                daily_mod.save_state(state)
                return 1
    daily_mod.save_state(state)
    return 0


def cmd_chart(argv: list[str]) -> int:
    challenge_id = ""
    metric = ""
    stat = "p99"
    rest = list(argv)
    while rest:
        tok = rest.pop(0)
        if tok == "--challenge" and rest:
            challenge_id = rest.pop(0)
        elif tok.startswith("--challenge="):
            challenge_id = tok.split("=", 1)[1]
        elif tok == "--metric" and rest:
            metric = rest.pop(0)
        elif tok.startswith("--metric="):
            metric = tok.split("=", 1)[1]
        elif tok == "--stat" and rest:
            stat = rest.pop(0)
        elif tok.startswith("--stat="):
            stat = tok.split("=", 1)[1]
        else:
            print(f"argumento desconhecido: {tok}", file=sys.stderr)
            return 2
    records = _records()
    pts = charts_mod.metric_series(
        records, challenge_id=challenge_id or None, metric=metric or None, stat=stat
    )
    label = metric or "auto"
    title = f"{challenge_id or 'todos'} · {label} · {stat} (n={len(pts)})"
    svg = charts_mod.line_chart_svg(pts, title=title)
    out = charts_dir() / f"curve-{(challenge_id or 'all')}-{label}-{stat}.svg"
    charts_mod.write_svg(out, svg)
    print(f"pontos: {len(pts)}")
    if len(pts) < 2:
        print("aviso: menos de 2 pontos — uma única execução não conta (§7); rode mais.")
    print(f"svg: {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(argv or [])
    if not args or args[0] in ("-h", "--help", "help"):
        print(_USAGE)
        return 0
    cmd, rest = args[0], args[1:]
    if cmd == "roadmap":
        return cmd_roadmap(rest)
    if cmd == "today":
        return cmd_today(rest)
    if cmd == "verify":
        return cmd_verify(rest)
    if cmd == "close":
        return cmd_close(rest)
    if cmd == "init":
        return cmd_init(rest)
    if cmd == "workdir":
        return cmd_workdir(rest)
    if cmd == "branch":
        return cmd_branch(rest)
    if cmd == "chart":
        return cmd_chart(rest)
    if cmd == "week":
        from edge_mage.roadmap.weekreport import cmd_week

        return cmd_week(rest)
    print(_USAGE, file=sys.stderr)
    return 2
