#!/usr/bin/env python3

from nicegui import ui

from . import doc


# Demo the ButtonToggle component
@doc.demo(ui.button_toggle)
def main_demo() -> None:
    toggle = ui.button_toggle(['Option A', 'Option B', 'Option C'], value='Option A')
    ui.label().bind_text_from(toggle, 'value', lambda v: f'Selected: {v}')


@doc.demo('Custom labels and values', '''
    You can provide options as dictionaries with separate labels and values.
''')
def dict_options() -> None:
    toggle = ui.button_toggle([
        {'label': 'Today', 'value': '1d'},
        {'label': 'This Week', 'value': '7d'},
        {'label': 'This Month', 'value': '30d'},
    ], value='7d').props('dense')
    ui.label().bind_text_from(toggle, 'value', lambda v: f'Selected: {v}')


@doc.demo('Toggle styling', '''
    You can apply the same styling options to a toggle as to a button, like "flat", "outline", "push", ...
''')
def styling() -> None:
    toggle = ui.button_toggle(['Small', 'Medium', 'Large'], value='Medium') \
        .props('color=secondary toggle-color=positive size=lg flat')
    ui.label().bind_text_from(toggle, 'value', lambda v: f'Selected: {v}')


@doc.demo('Programmatic control', '''
    You can programmatically change the selected value and get notified of changes.
''')
def programmatic_control() -> None:
    toggle = ui.button_toggle(['Red', 'Green', 'Blue'], value='Red',
                       on_change=lambda e: ui.notify(f'Selection changed to: {e.value}'))

    with ui.row().classes('gap-2 mt-2'):
        ui.button('Set to Green', on_click=lambda: toggle.set_value('Green'))
        ui.button('Set to Blue', on_click=lambda: toggle.set_value('Blue'))
        ui.button('Get Value', on_click=lambda: ui.notify(f'Current value: {toggle.value}'))


doc.reference(ui.button_toggle)
