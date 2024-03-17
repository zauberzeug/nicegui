#!/usr/bin/env python3
from pathlib import Path

from nicegui import ui


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
    await ui.run_javascript('disconnect()', timeout=5)
    state['connected'] = False

state = {'connected': False}

ui.add_body_html(f'<script>{(Path(__file__).parent / "script.js").read_text()}</script>')

ui.button('Connect', on_click=connect).bind_enabled_from(state, 'connected', lambda connected: not connected)
ui.button('LED On', on_click=lambda: ui.run_javascript('send("1")')).bind_enabled_from(state, 'connected')
ui.button('LED Off', on_click=lambda: ui.run_javascript('send("0")')).bind_enabled_from(state, 'connected')
ui.button('Disconnect', on_click=disconnect).bind_enabled_from(state, 'connected')

ui.on('read', lambda counts: ui.notify(f'Button pressed {counts} times!'))

ui.run()
