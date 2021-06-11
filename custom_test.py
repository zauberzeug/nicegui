#!/usr/bin/env python3
from nicegui import ui

with ui.card():
    example = ui.custom_example(on_change=lambda number: label.set_text(f'Custom value: {number}'))

ui.button('Add 100', on_click=lambda: example.add(100))

label = ui.label()

ui.joystick(on_move=lambda e: print("move", e.data.vector), color='blue', size=50)
