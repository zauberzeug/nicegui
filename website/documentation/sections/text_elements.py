from nicegui import ui

from ..tools import load_demo


def content() -> None:
    load_demo(ui.label)
    load_demo(ui.link)
    load_demo(ui.chat_message)
    load_demo(ui.element)
    load_demo(ui.markdown)
    load_demo(ui.mermaid)
    load_demo(ui.html)
