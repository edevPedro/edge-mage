"""Testes do parser de comandos colon."""

from __future__ import annotations

import pytest

from edge_mage.commands import KNOWN_COMMANDS, help_text, parse_command


@pytest.mark.parametrize(
    "line,name,args",
    [
        (":q", "quit", ()),
        ("q", "quit", ()),
        (":sair", "quit", ()),
        (":tracks", "tracks", ()),
        (":trilhas", "tracks", ()),
        (":profile", "profile", ()),
        (":perfil", "profile", ()),
        (":home", "home", ()),
        (":xp", "xp", ()),
        (":help", "help", ()),
        (":ajuda", "help", ()),
        (":room trigonometria", "room", ("trigonometria",)),
        (":sala ohm", "room", ("ohm",)),
        ("  :q  ", "quit", ()),
    ],
)
def test_parse_ok(line: str, name: str, args: tuple[str, ...]) -> None:
    cmd = parse_command(line)
    assert cmd.error is None
    assert cmd.name == name
    assert cmd.args == args


def test_parse_empty() -> None:
    cmd = parse_command(":")
    assert cmd.error
    assert cmd.name == ""


def test_parse_unknown() -> None:
    cmd = parse_command(":foo")
    assert cmd.error
    assert "desconhecido" in cmd.error


def test_parse_room_requires_id() -> None:
    cmd = parse_command(":room")
    assert cmd.error
    assert "uso" in cmd.error


def test_help_mentions_bindings() -> None:
    text = help_text()
    assert ":q" in text
    assert "j / k" in text
    assert "g p" in text
    assert "NORMAL" in text
    assert "INSERT" in text
    assert ":anim" in text
    for name in ("quit", "tracks", "profile", "room", "help", "xp", "anim", "sync"):
        assert name in KNOWN_COMMANDS


def test_parse_anim() -> None:
    cmd = parse_command(":anim unit_circle")
    assert cmd.error is None
    assert cmd.name == "anim"
    assert cmd.args == ("unit_circle",)
