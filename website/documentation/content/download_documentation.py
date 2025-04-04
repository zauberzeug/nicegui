from nicegui import ui

from . import doc


@doc.demo(ui.download)
def main_demo() -> None:
    ui.button('Local file', on_click=lambda: ui.download.file('main.py'))
    ui.button('From URL', on_click=lambda: ui.download.from_url('https://nicegui.io/logo.png'))
    ui.button('Content', on_click=lambda: ui.download.content('Hello World', 'hello.txt'))


@doc.demo(ui.download.from_url)
def from_url_demo() -> None:
    ui.button('Download', on_click=lambda: ui.download.from_url('https://nicegui.io/logo.png'))


@doc.demo(ui.download.content)
def content_demo() -> None:
    ui.button('Download', on_click=lambda: ui.download.content('Hello World', 'hello.txt'))


@doc.demo(ui.download.file)
def file_demo() -> None:
    ui.button('Download', on_click=lambda: ui.download.file('main.py'))
