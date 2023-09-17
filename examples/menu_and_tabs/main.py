#!/usr/bin/env python3
from nicegui import ui

# header layout
with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as _tabs:
        ui.tab('A')
        ui.tab('B')
        ui.tab('C')

with ui.tab_panels(_tabs, value='B').classes('w-full'):
    with ui.tab_panel('A'):
        ui.label('Content of A')
    with ui.tab_panel('B'):
        ui.label('Content of B')
    with ui.tab_panel('C'):
        ui.label('Content of C')

# sidebar
with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Side menu')

# bottom layout
with ui.footer(value=False) as _footer:
    ui.label('Footer Area')

# stick to control _footer
with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=_footer.toggle, icon='contact_support').props('fab')


ui.run()
