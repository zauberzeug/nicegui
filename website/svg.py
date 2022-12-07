from pathlib import Path

from nicegui import ui

PATH = Path(__file__).parent / 'static'


def _svg(name: str) -> ui.html:
    return ui.html((PATH / f'{name}.svg').read_text())


def face() -> ui.html:
    return _svg('happy_face')


def word() -> ui.html:
    return _svg('nicegui_word')


def github() -> ui.html:
    return _svg('github')
