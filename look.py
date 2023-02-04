#!/usr/bin/env python3
from nicegui import ui

with ui.row().looks.width.full().background.primary().padding.two().align.main_axis.center().element:
    for i in range(5):
        with ui.card():
            ui.label(str(i))

ui.button('looks great').looks.width.full()

ui.run()
