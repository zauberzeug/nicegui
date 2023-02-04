#!/usr/bin/env python3
from nicegui import Looks, ui

with ui.row().looks.width.full().background.secondary().padding.y_axis.small().align.main_axis.center().element:
    for i in range(5):
        with ui.card():
            ui.label(str(i))

shared = Looks().background.teal(0.9)

with ui.row().looks.width.full().element:
    ui.button('12').looks.width.fixed.twelve().extend(shared)
    ui.button('64').looks.width.fixed.sixty_four().extend(shared)
    ui.button('1/6').looks.width.fractional.one_sixth().on_hover().text.gray(0.6)

ui.run()
