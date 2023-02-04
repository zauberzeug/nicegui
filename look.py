#!/usr/bin/env python3
from nicegui import ui

with ui.row().classes('w-full bg-primary p-2 justify-center'):
    for i in range(5):
        with ui.card().classes(''):
            ui.label(str(i))

ui.run()
