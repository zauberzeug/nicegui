#!/usr/bin/env python3
from nicegui import Looks, ui

with ui.row().apply(Looks().w.full().bg.primary().p.two().align.main_axis.center()):
    for i in range(5):
        with ui.card():
            ui.label(str(i))

ui.run()
