from nicegui import ui

from ..tools import load_demo

name = 'text_elements'
title = 'Text Elements'
description = '''
    Elements like `ui.label`, `ui.markdown` and `ui.html` can be used to display text and other content.
'''


def content() -> None:
    load_demo(ui.label)
    load_demo(ui.link)
    load_demo(ui.chat_message)
    load_demo(ui.element)
    load_demo(ui.markdown)
    load_demo(ui.mermaid)
    load_demo(ui.html)
