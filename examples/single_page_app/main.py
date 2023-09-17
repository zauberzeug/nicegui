#!/usr/bin/env python3
from nicegui import ui

from router import Router
from pathlib import Path

@ui.page('/')  # normal index page (e.g. the entry point of the app)
@ui.page('/{_:path}')  # all other pages will be handled by the router but must be registered to also show the SPA index page
def main():
    router = Router()

    @router.add('/')
    @router.add('/one')
    def show_one():
        ui.label('😊 NiceGUI demos').classes('text-2xl')
        file_md = Path("../nicegui_demos.md")
        ui.markdown(open(file_md).read())

    @router.add('/two')
    def show_two():
        ui.label('Content Two').classes('text-2xl')

    @router.add('/three')
    def show_three():
        ui.label('Content Three').classes('text-2xl')

    # adding some navigation buttons to switch between the different pages
    with ui.row():
        ui.button('Demos', on_click=lambda: router.open(show_one)).classes('w-32')
        ui.button('Two', on_click=lambda: router.open(show_two)).classes('w-32')
        ui.button('Three', on_click=lambda: router.open(show_three)).classes('w-32')

    ui.label("Welcome to NiceGUI")

    # this places the content which should be displayed
    router.frame().classes('w-full p-4 bg-gray-100')


ui.run()
