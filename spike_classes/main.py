#!/usr/bin/env python3
from nicegui import ui

ui.label('Hello world!')
ui.button('Click me')

with ui.row():
    ui.label('left')
    ui.label('right')

t = ui.label('Timer')
ui.timer(1.0, lambda: setattr(t.view, 'text', t.view.text + '.'))
