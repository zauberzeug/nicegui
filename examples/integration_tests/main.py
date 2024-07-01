#!/usr/bin/env python3
from nicegui import Client, ui

# pylint: disable=missing-function-docstring


@ui.page('/')
def main_page() -> None:
    ui.markdown('Try running `pytest` on this project!')
    ui.button('Click me', on_click=lambda: ui.notify('Button clicked!'))


@ui.page('/subpage')
def sub_page() -> None:
    ui.markdown('This is a subpage')


@ui.page('/with_connected')
async def with_connected(client: Client) -> None:
    ui.markdown('This is an async connection demo')
    await client.connected()
    ui.markdown('Connected!')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
