#!/usr/bin/env python3
from nicegui import ui


@ui.page('/')  # normal index page (e.g. the entry point of the app)
@ui.page('/{_:path}')  # all other pages will be handled by the router but must be registered to also show the SPA index page
def main_page():

    # adding some navigation buttons to switch between the different pages
    with ui.row():
        ui.button('One', on_click=lambda: ui.navigate.to('/')).classes('w-32')
        ui.button('Two', on_click=lambda: ui.navigate.to('/two')).classes('w-32')
        ui.button('Three', on_click=lambda: ui.navigate.to('/three')).classes('w-32')

    # depending on the url path, the corresponding page will be displayed
    ui.sub_pages({
        '/': show_one,
        '/two': show_two,
        '/three': show_three,
    }).classes('w-full p-4 bg-gray-100')


def show_one():
    ui.label('Content One').classes('text-2xl')


def show_two():
    ui.label('Content Two').classes('text-2xl')


def show_three():
    ui.label('Content Three').classes('text-2xl')


ui.run()
