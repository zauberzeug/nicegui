#!/usr/bin/env python3
"""Demonstrates input_chips blur functionality.

This example shows how input_chips automatically adds typed values as chips
when the field loses focus (blur event), in addition to the default Enter key behavior.
"""
from nicegui import ui

ui.markdown('## Input Chips with Blur Support')
ui.markdown('''
Type a value and press **Tab** or **click elsewhere** to add it as a chip.
The **Enter** key also works (original behavior).
''')

ui.separator()

# Toggle mode (default)
with ui.card().classes('w-full'):
    ui.label('Toggle Mode (default)').classes('text-h6')
    ui.markdown('Adding the same value twice **removes** it.')
    chips_toggle = ui.input_chips(label='Try typing "test" twice', new_value_mode='toggle')
    ui.label().bind_text_from(chips_toggle, 'value', lambda v: f'Chips: {v}')

ui.separator()

# Add mode
with ui.card().classes('w-full'):
    ui.label('Add Mode').classes('text-h6')
    ui.markdown('**Allows duplicate** values.')
    chips_add = ui.input_chips(label='Try typing "test" twice', new_value_mode='add')
    ui.label().bind_text_from(chips_add, 'value', lambda v: f'Chips: {v}')

ui.separator()

# Add-unique mode
with ui.card().classes('w-full'):
    ui.label('Add-Unique Mode').classes('text-h6')
    ui.markdown('**Prevents duplicate** values.')
    chips_unique = ui.input_chips(label='Try typing "test" twice', new_value_mode='add-unique')
    ui.label().bind_text_from(chips_unique, 'value', lambda v: f'Chips: {v}')

ui.separator()

ui.button('Click to trigger blur', icon='touch_app')

ui.run(port=8087)
