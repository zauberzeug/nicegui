#!/usr/bin/env python3
from typing import Dict

from nicegui import ui

tab_names = ['A', 'B', 'C']

# necessary until we improve native support for tabs (https://github.com/zauberzeug/nicegui/issues/251)


def switch_tab(msg: Dict) -> None:
    name = msg['args']
    tabs.props(f'model-value={name}')
    panels.props(f'model-value={name}')


with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=menu')
    with ui.element('q-tabs').on('update:model-value', switch_tab) as tabs:
        for name in tab_names:
            ui.element('q-tab').props(f'name={name} label={name}')

with ui.footer(value=False) as footer:
    ui.label('Footer')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Side menu')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle).props('fab icon=contact_support')


# the page content consists of multiple tab panels
with ui.element('q-tab-panels').props('model-value=A animated').classes('w-full') as panels:
    for name in tab_names:
        with ui.element('q-tab-panel').props(f'name={name}').classes('w-full'):
            ui.label(f'Content of {name}')

ui.run()
