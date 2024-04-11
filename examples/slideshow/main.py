#!/usr/bin/env python3
from pathlib import Path

from nicegui import app, ui
from nicegui.events import KeyEventArguments

ui.query('.nicegui-content').classes('p-0')  # remove padding from the main content

folder = Path(__file__).parent / 'slides'  # image source: https://pixabay.com/
files = sorted(f.name for f in folder.glob('*.jpg'))
state = {'index': 0}


def handle_key(event: KeyEventArguments) -> None:
    if event.action.keydown:
        if event.key.arrow_right:
            state['index'] += 1
        if event.key.arrow_left:
            state['index'] -= 1
        state['index'] %= len(files)
        slide.set_source(f'slides/{files[state["index"]]}')


app.add_static_files('/slides', folder)  # serve all files in this folder
slide = ui.image(f'slides/{files[state["index"]]}')  # show the first image
ui.keyboard(on_key=handle_key)  # handle keyboard events

ui.run()
