from pathlib import Path

from nicegui import ui

PATH = Path(__file__).parent / 'static'
HAPPY_FACE_SVG = (PATH / 'happy_face.svg').read_text()
NICEGUI_WORD_SVG = (PATH / 'nicegui_word.svg').read_text()
GITHUB_SVG = (PATH / 'github.svg').read_text()
DISCORD_SVG = (PATH / 'discord.svg').read_text()
REDDIT_SVG = (PATH / 'reddit.svg').read_text()


def face(half: bool = False) -> ui.html:
    code = HAPPY_FACE_SVG
    if half:
        code = code.replace('viewBox="0 0 62.44 71.74"', 'viewBox="31.22 0 31.22 71.74"')
    return ui.html(code)


def word() -> ui.html:
    return ui.html(NICEGUI_WORD_SVG)


def github() -> ui.html:
    return ui.html(GITHUB_SVG)


def discord() -> ui.html:
    return ui.html(DISCORD_SVG)


def reddit() -> ui.html:
    return ui.html(REDDIT_SVG)
