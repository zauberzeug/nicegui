#!/usr/bin/env python3
from local_file_picker import local_file_picker

from nicegui import ui


async def pick_file() -> None:
    result = await local_file_picker('~', multiple=True)
    ui.notify(f'You chose {result}')


@ui.page('/')
def index():
    ui.button('Choose file', on_click=pick_file, icon='folder')


ui.run()
