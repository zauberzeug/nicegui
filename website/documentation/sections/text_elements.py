from nicegui import ui

from ..tools import load_demo, section_intro_demo

name = 'text_elements'
title = 'Text Elements'


def intro() -> None:
    @section_intro_demo(name, title, '''
        NiceGUI provides a set of text elements to display text and other content.
        The most basic element is the `ui.label`, which can be used to display a simple text.
        But there are also more advanced elements, such as `ui.markdown`, `ui.mermaid` and `ui.html`.
    ''')
    def label():
        ui.label('Hello, world!')
        ui.markdown('This is **Markdown**.')
        ui.html('This is <strong>HTML</strong>.')


def content() -> None:
    load_demo(ui.label)
    load_demo(ui.link)
    load_demo(ui.chat_message)
    load_demo(ui.element)
    load_demo(ui.markdown)
    load_demo(ui.mermaid)
    load_demo(ui.html)
