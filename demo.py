#!/usr/bin/env python3
from examples.custom_vue_component.counter import Counter
from examples.custom_vue_component.fireworks import Fireworks
from examples.custom_vue_component.on_off import OnOff
from nicegui import ui

with ui.row(align_items='center'):
    counter = Counter('Count', on_change=lambda e: ui.notify(f'The value changed to {e.args}.'))
    ui.button('Reset', on_click=counter.reset).props('outline')

with ui.row(align_items='center'):
    on_off = OnOff('State', on_change=lambda e: ui.notify(f'The value changed to {e.args}.'))
    ui.button('Reset', on_click=on_off.reset).props('outline')

with ui.column(align_items='center'):
    ui.label('Fireworks Demo').classes('text-2xl')

    with ui.row(align_items='center'):
        fireworks = Fireworks()
        # Add controls in a card
    with ui.card().classes('w-full'):
        with ui.row().classes('w-full'):
            ui.label("Gravity")
            ui.slider(min=0.1, max=3.0, step=0.1, value=fireworks._props['gravity']).props('label="Gravity"')
            ui.label("Opacity")
            ui.slider(min=0.1, max=1.0, step=0.1, value=fireworks._props['opacity']).props('label="Opacity"')
            ui.label("Acceleration")
            def update_acceleration(e):
                fireworks.update_options(acceleration=e.value)
            ui.slider(min=0.1, max=2.0, step=0.1, value=fireworks._props['acceleration'], on_change=update_acceleration).props('label="Acceleration"')

    ui.button('Start', on_click=fireworks.start).props('outline')
    ui.button('Stop', on_click=fireworks.stop).props('outline')
ui.run(port=9001, prod_js=False, uvicorn_reload_includes='*.py,*.js,*.vue')


ui.run()
