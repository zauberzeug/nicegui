import os
from pathlib import Path

from nicegui import ui
from nicegui.elements.keyboard import KeyEventArguments

index = 0
# NOTE the images are taken from https://pixabay.com/
folder = Path(__file__).resolve().parent / 'slides'
files = sorted([f.name for f in folder.glob('**/*.jpg')])


def handle_key(event: KeyEventArguments):
    global index
    if event.action.keydown:
        if event.key.arrow_right:
            index += 1
        if event.key.arrow_left:
            index -= 1
        index = index % len(files)
        slide.set_source(f'slides/{files[index]}')


ui.add_static_files('/slides', folder)  # serve all files in this folder
slide = ui.image('slides/' + files[index])  # show the first image
ui.keyboard(on_key=handle_key)  # handle keyboard events

ui.run()
