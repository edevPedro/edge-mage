"""CLI `mage lab` — listar, iniciar, rodar e inspecionar labs verificáveis."""

from __future__ import annotations

import json
import sys

_USAGE = """uso: mage lab <comando> [args]

comandos:
  list              lista os labs disponíveis
  init <lab>        cria o diretório de trabalho (~/.mage/labs/<lab>/work)
  run <lab>         compila, testa, mede e grava evidência em ~/.mage/evidence/
  latest <lab>      mostra a última evidência registrada
"""


def _cmd_list(argv: list[str]) -> int:
    from edge_mage.labs import available_labs, has_cpp_toolchain, load_spec

    labs = available_labs()
    if not labs:
        print("nenhum lab em content/labs/")
        return 0
    if not has_cpp_toolchain():
        print(
            "aviso: nenhum compilador C++ (clang++/g++) encontrado",
            file=sys.stderr,
        )
    for lab_id in labs:
        try:
            spec = load_spec(lab_id)
            title = spec.title
        except Exception as exc:  # noqa: BLE001
            title = f"spec inválida: {exc}"
        print(f"  {lab_id:16s} {title}")
    return 0


def _cmd_init(argv: list[str]) -> int:
    from edge_mage.labs import init_lab

    lab_id = argv[0]
    work, copied = init_lab(lab_id, force="--force" in argv)
    print(f"work dir: {work}")
    if copied:
        print("arquivos criados: " + ", ".join(copied))
    else:
        print("nada novo (use --force para sobrescrever)")
    return 0


def _cmd_run(argv: list[str]) -> int:
    from edge_mage.labs import format_result, run_lab

    result = run_lab(argv[0])
    print(format_result(result))
    return 0 if result.ok else 1


def _cmd_latest(argv: list[str]) -> int:
    from edge_mage.labs import read_latest

    record = read_latest(argv[0])
    if not record:
        print(f"sem evidência — rode `mage lab run {argv[0]}`")
        return 1
    print(json.dumps(record, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(argv or [])
    if not args or args[0] in ("-h", "--help", "help"):
        print(_USAGE)
        return 0
    cmd, rest = args[0], args[1:]
    if cmd == "list":
        return _cmd_list(rest)
    if cmd == "init":
        if not rest:
            print("uso: mage lab init <lab>", file=sys.stderr)
            return 2
        return _cmd_init(rest)
    if cmd == "run":
        if not rest:
            print("uso: mage lab run <lab>", file=sys.stderr)
            return 2
        return _cmd_run(rest)
    if cmd == "latest":
        if not rest:
            print("uso: mage lab latest <lab>", file=sys.stderr)
            return 2
        return _cmd_latest(rest)
    print(_USAGE, file=sys.stderr)
    return 2
