from pathlib import Path

from nicegui import ui

PATH = Path(__file__).parent / 'static'


def face(half: bool = False) -> ui.html:
    code = (PATH / 'happy_face.svg').read_text()
    if half:
        code = code.replace('viewBox="0 0 62.44 71.74"', 'viewBox="31.22 0 31.22 71.74"')
    return ui.html(code)


def word() -> ui.html:
    return ui.html((PATH / 'nicegui_word.svg').read_text())


def github() -> ui.html:
    return ui.html((PATH / 'github.svg').read_text())


def discord() -> ui.html:
    return ui.html((PATH / 'discord.svg').read_text())


def reddit() -> ui.html:
    return ui.html((PATH / 'reddit.svg').read_text())
