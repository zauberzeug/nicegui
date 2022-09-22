#!/usr/bin/env python3
from pathlib import Path

from nicegui import ui
from nicegui.events import KeyEventArguments

folder = Path(__file__).resolve().parent / 'slides'  # image source: https://pixabay.com/
files = sorted(f.name for f in folder.glob('*.jpg'))
index = 0


def handle_key(event: KeyEventArguments) -> None:
    global index
    if event.action.keydown:
        if event.key.arrow_right:
            index += 1
        if event.key.arrow_left:
            index -= 1
        index = index % len(files)
        slide.set_source(f'slides/{files[index]}')


ui.add_static_files('/slides', folder)  # serve all files in this folder
slide = ui.image(f'slides/{files[index]}')  # show the first image
ui.keyboard(on_key=handle_key)  # handle keyboard events

ui.run()
