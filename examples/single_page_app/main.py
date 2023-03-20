#!/usr/bin/env python3

from router import Router

from nicegui import ui

router = Router()


@router.add('/')
async def show_one():
    ui.label('Content One').classes('text-2xl')


@router.add('/two')
async def show_two():
    ui.label('Content Two').classes('text-2xl')


@router.add('/three')
async def show_three():
    ui.label('Content Three').classes('text-2xl')


with ui.row():
    ui.button('One', on_click=lambda: router.open(show_one)).classes('w-32')
    ui.button('Two', on_click=lambda: router.open(show_two)).classes('w-32')
    ui.button('Three', on_click=lambda: router.open(show_three)).classes('w-32')

# this places the frame for the content which should be displayed
router.frame().classes('w-full pt-8')

ui.run()
