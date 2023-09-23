#!/usr/bin/env python3
from pathlib import Path

from nicegui import app, ui
from nicegui.events import KeyEventArguments

ui.query('.nicegui-content').classes('p-0')  # remove padding from the main content

def glob_img_files(folder, types=["jpg","png"]):
    files = []
    for f in folder.glob("*"):
        for _type in types:
            if f.name.lower().endswith(_type):
                files.append(f.name)
    return sorted(files)

folder = Path(__file__).parent / 'slides'  # image source: https://pixabay.com/
# files = sorted(f.name for f in folder.glob('*.jpg'))
files = glob_img_files(folder)
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



app.add_static_files('/slides', folder)  # serve all files in this folder
slide = ui.image(f'slides/{files[index]}')  # show the first image
ui.keyboard(on_key=handle_key)  # handle keyboard events

ui.run()
