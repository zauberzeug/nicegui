#!/usr/bin/env python3
from counter import Counter
from on_off import OnOff

from nicegui import ui

with ui.row(align_items='center'):
    counter = Counter('Count', on_change=lambda e: ui.notify(f'The value changed to {e.args}.'))
    ui.button('Reset', on_click=counter.reset).props('outline')

with ui.row(align_items='center'):
    on_off = OnOff('State', on_change=lambda e: ui.notify(f'The value changed to {e.args}.'))
    ui.button('Reset', on_click=on_off.reset).props('outline')


ui.run(uvicorn_reload_includes='*.py,*.js,*.vue')
