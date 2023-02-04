#!/usr/bin/env python3
from nicegui import ui

with ui.row().looks.w.full().bg.primary().p.two().align.main_axis.center().element:
    for i in range(5):
        with ui.card():
            ui.label(str(i))

ui.button('looks great').looks.w.full()

ui.run()
