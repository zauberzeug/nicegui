from pathlib import Path

from nicegui import app, ui

PATH = Path(__file__).parent / 'static'
HAPPY_FACE_SVG = (PATH / 'happy_face.svg').read_text(encoding='utf-8')
NICEGUI_WORD_SVG = (PATH / 'nicegui_word.svg').read_text(encoding='utf-8')
GITHUB_SVG = (PATH / 'github.svg').read_text(encoding='utf-8')
DISCORD_SVG = (PATH / 'discord.svg').read_text(encoding='utf-8')
REDDIT_SVG = (PATH / 'reddit.svg').read_text(encoding='utf-8')

app.browser_data_store['happy_face_svg'] = HAPPY_FACE_SVG
app.browser_data_store['nicegui_word_svg'] = NICEGUI_WORD_SVG
app.browser_data_store['github_svg'] = GITHUB_SVG
app.browser_data_store['discord_svg'] = DISCORD_SVG
app.browser_data_store['reddit_svg'] = REDDIT_SVG

app.browser_data_store['half_happy_face_svg'] = HAPPY_FACE_SVG.replace(
    'viewBox="0 0 62.44 71.74"', 'viewBox="31.22 0 31.22 71.74"')


def face(half: bool = False) -> ui.html:
    if half:
        return ui.html(ui.context.client.fetch_string_from_browser_data_store('half_happy_face_svg'))
    return ui.html(ui.context.client.fetch_string_from_browser_data_store('happy_face_svg'))


def word() -> ui.html:
    return ui.html(ui.context.client.fetch_string_from_browser_data_store('nicegui_word_svg'))


def github() -> ui.html:
    return ui.html(ui.context.client.fetch_string_from_browser_data_store('github_svg'))


def discord() -> ui.html:
    return ui.html(ui.context.client.fetch_string_from_browser_data_store('discord_svg'))


def reddit() -> ui.html:
    return ui.html(ui.context.client.fetch_string_from_browser_data_store('reddit_svg'))
