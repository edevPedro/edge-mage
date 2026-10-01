"""Tema terminal nítido para o Edge Mage (sem glow)."""

THEME_CSS = """
Screen {
    background: #0b0d10;
    color: #c4cad1;
}

#banner {
    color: #c8d0d6;
    text-align: center;
    padding: 1 0;
}

.title {
    color: #e6eaee;
    text-style: bold;
    padding: 0 1;
}

.muted {
    color: #6b737c;
}

.accent {
    color: #9db8a5;
}

.warn {
    color: #c9a227;
}

.ok {
    color: #8fbc8f;
}

.err {
    color: #c97070;
}

.rank {
    color: #c9a227;
    text-style: bold;
}

Button {
    margin: 0 1 1 0;
}

Button.-primary {
    background: #1a2420;
    color: #c8d0d6;
    border: tall #3a4a42;
}

Button.-primary:hover {
    background: #24322c;
}

Button.-danger {
    background: #2a1818;
    color: #c97070;
}

ListView {
    border: solid #2a3038;
    height: 1fr;
    background: #0e1115;
}

OptionList {
    border: solid #2a3038;
    height: 1fr;
    background: #0e1115;
}

ListItem {
    padding: 0 1;
}

ListItem:hover {
    background: #161a20;
}

ListItem.-highlight {
    background: #1c2420;
}

.panel {
    border: solid #2a3038;
    background: #0e1115;
    padding: 1 2;
    margin: 0 1 1 1;
    height: auto;
}

.panel-title {
    color: #9db8a5;
    text-style: bold;
    margin-bottom: 1;
}

Markdown {
    height: auto;
    padding: 0 1;
}

Input, TextArea {
    border: solid #2a3038;
    background: #0e1115;
}

Input:focus, TextArea:focus {
    border: solid #5a6570;
}

#status {
    height: auto;
    padding: 0 1;
}

#xp-bar {
    height: 1;
    margin: 0 1 1 1;
    color: #9db8a5;
}

.locked {
    color: #555c64;
}

.done {
    color: #8fbc8f;
}

#help-body {
    height: auto;
}

#room-main {
    height: 14;
    margin: 0 0 1 0;
}

#room-main #pane-story,
#room-main #pane-concept,
#room-main #pane-desafio {
    width: 1fr;
    height: 1fr;
    margin: 0 1 0 1;
}

#room-main .-hidden-pane {
    display: none;
}

#room-main AnimationPanel {
    width: 42;
    height: 1fr;
}

.tab-bar {
    color: #9db8a5;
    padding: 0 1;
    margin-bottom: 0;
}

.-pane-focus {
    border: solid #5a7a68 !important;
}

#home-menu, #track-list, #room-list, #task-list, #task-actions {
    height: 1fr;
    margin: 0 1 1 1;
}

#help-actions, #profile-actions, #grimoire-actions {
    height: auto;
    max-height: 5;
    margin: 0 1 1 1;
}
"""
