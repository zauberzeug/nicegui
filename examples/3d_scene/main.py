#!/usr/bin/env python3
from nicegui import app, ui

app.add_static_files('/stl', 'static')

with ui.scene(width=1024, height=800) as scene:
    scene.stl('/stl/pikachu.stl').move(x=-0.5).scale(0.06)

ui.run()
