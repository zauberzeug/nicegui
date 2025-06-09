from pathlib import Path

from nicegui import ui

PATH = Path(__file__).parent / 'static'
HAPPY_FACE_SVG = (PATH / 'happy_face.svg').read_text(encoding='utf-8')
HALF_HAPPY_FACE_SVG = HAPPY_FACE_SVG.replace('viewBox="0 0 62.44 71.74"', 'viewBox="31.22 0 31.22 71.74"')
NICEGUI_WORD_SVG = (PATH / 'nicegui_word.svg').read_text(encoding='utf-8')
GITHUB_SVG = (PATH / 'github.svg').read_text(encoding='utf-8')
DISCORD_SVG = (PATH / 'discord.svg').read_text(encoding='utf-8')
REDDIT_SVG = (PATH / 'reddit.svg').read_text(encoding='utf-8')


def face(half: bool = False) -> ui.html:
    if half:
        return ui.html(HALF_HAPPY_FACE_SVG).cache('half-happy-face-svg')
    else:
        happy_face_svg_element = ui.html(HAPPY_FACE_SVG)
        happy_face_svg_element.dynamic_keys.add('class')  # allow different classes across caches
        happy_face_svg_element.static_prop_keys.add('innerHTML')
        happy_face_svg_element.cache('happy-face-svg')
        return happy_face_svg_element


def word() -> ui.html:
    word_svg_element = ui.html(NICEGUI_WORD_SVG)
    word_svg_element.static_prop_keys.add('innerHTML')
    return word_svg_element.cache('word-svg')


def github() -> ui.html:
    github_svg_element = ui.html(GITHUB_SVG)
    github_svg_element.static_prop_keys.add('innerHTML')
    return github_svg_element.cache('github-svg')


def discord() -> ui.html:
    discord_svg_element = ui.html(DISCORD_SVG)
    discord_svg_element.static_prop_keys.add('innerHTML')
    return discord_svg_element.cache('discord-svg')


def reddit() -> ui.html:
    reddit_svg_element = ui.html(REDDIT_SVG)
    reddit_svg_element.static_prop_keys.add('innerHTML')
    return reddit_svg_element.cache('reddit-svg')
