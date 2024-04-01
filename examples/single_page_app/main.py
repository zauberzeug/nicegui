#!/usr/bin/env python3
from router import Router

from nicegui import ui


def add_links():
    ui.link('One', '/')
    ui.link('Two', '/two')
    ui.link('Three', '/three')
    ui.link('Four', '/four')


@ui.page('/four')  # normal index page (e.g. the entry point of the app)
def show_four():
    ui.label('Content Four').classes('text-2xl')
    add_links()


@ui.page('/')  # normal index page (e.g. the entry point of the app)
def main():
    router = Router()

    @router.add('/')
    def show_one():
        ui.label('Content One').classes('text-2xl')
        add_links()

    @router.add('/two')
    def show_two():
        ui.label('Content Two').classes('text-2xl')
        add_links()

    @router.add('/three')
    def show_three():
        ui.label('Content Three').classes('text-2xl')
        add_links()

    # this places the content which should be displayed
    router.frame().classes('w-full p-4 bg-gray-100')


ui.run(show=False)
