#!/usr/bin/env python3
from vue_vite.counters import CounterComposition, CounterOptions

from nicegui import ui

with ui.row(align_items='center'):
    counter = CounterOptions('Options', on_change=lambda e: ui.notify(f'Options value changed to {e.args}'))
    ui.button('Reset', on_click=counter.reset).props('outline')

with ui.row(align_items='center'):
    counter = CounterComposition('Composition', on_change=lambda e: ui.notify(f'Composition value changed to {e.args}'))
    ui.button('Reset', on_click=counter.reset).props('outline')

ui.run(uvicorn_reload_includes='*.py,*.js,*.vue')
