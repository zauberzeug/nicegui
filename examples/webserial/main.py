#!/usr/bin/env python3
from pathlib import Path

from nicegui import ui


@ui.page('/')
def page():
    async def connect() -> None:
        if not await ui.run_javascript('"serial" in navigator'):
            ui.notify('WebSerial is not available in this browser.')
            return

        if not await ui.run_javascript('connect()', timeout=100):
            ui.notify('Could not connect to the device.')
            return

        ui.run_javascript('readLoop()')
        state['connected'] = True

    async def disconnect() -> None:
        ui.run_javascript('disconnect()', timeout=5)
        state['connected'] = False

    state = {
        'connected': False,
        'button': False,
    }

    ui.add_body_html(f'<script>{(Path(__file__).parent / "script.js").read_text(encoding="utf-8")}</script>')

    ui.button('Connect', on_click=connect).bind_visibility_from(state, 'connected', value=False)
    ui.button('Disconnect', on_click=disconnect).bind_visibility_from(state, 'connected')
    ui.switch('LED', on_change=lambda e: ui.run_javascript(f'send({e.value:d})')).bind_enabled_from(state, 'connected')
    ui.switch('Button').props('disable').bind_value_from(state, 'button')

    ui.on('read', lambda e: state.update(button=e.args == 'LOW'))


ui.run()
