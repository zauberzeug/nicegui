#!/usr/bin/env python3
from nicegui import ui

with ui.row().looks.width.full().background.primary().padding.two().align.main_axis.center().element:
    for i in range(5):
        with ui.card():
            ui.label(str(i))

with ui.row().looks.width.full().element:
    ui.button('12').looks.width.fixed.twelve()
    ui.button('64').looks.width.fixed.sixty_four()
    ui.button('1/6').looks.width.fractional.one_sixth()

ui.run()
