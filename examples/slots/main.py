#!/usr/bin/env python3
from nicegui import ui

tree = ui.tree([
    {'id': 'numbers', 'icon': 'tag', 'children': [{'id': '1'}, {'id': '2'}]},
    {'id': 'letters', 'icon': 'text_fields', 'children': [{'id': 'A'}, {'id': 'B'}]},
], label_key='id', on_select=lambda e: ui.notify(e.value))

with tree.add_slot('default-header'):
    with ui.row(align_items='center').classes('gap-2'):
        ui.icon('', color='orange', size='28px').props(''' :name="props.node.icon || 'share'" ''')
        ui.label().props(':innerHTML=props.node.id').classes('text-weight-bold text-primary')

with tree.add_slot('default-body'):
    ui.label('This is some default content.').classes('ml-8 text-weight-light text-black')

ui.run()
