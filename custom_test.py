#!/usr/bin/env python3
from nicegui import ui

with ui.card():
    example = ui.custom_example(on_change=lambda number: label.set_text(f'Custom value: {number}'))

ui.button('Add 100', on_click=lambda: example.add(100))

label = ui.label()

ui.joystick(on_move=lambda e: print("move", e.vector))

three = ui.three(on_click=lambda e: print("click", e))
ui.slider(min=0, max=10, on_change=lambda e: three.move_camera(e.value))
