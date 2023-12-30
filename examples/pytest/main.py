#!/usr/bin/env python3
from nicegui import ui


@ui.page('/')
def main_page() -> None:
    ui.markdown('Try running `pytest` on this project!')
    ui.button('Click me', on_click=lambda: ui.notify('Button clicked!'))


if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
