#!/usr/bin/env python3
from nicegui import ui

tree = ui.tree([
    {'id': 'numbers', 'icon': 'tag', 'children': [{'id': '1'}, {'id': '2'}]},
    {'id': 'letters', 'icon': 'text_fields', 'children': [{'id': 'A'}, {'id': 'B'}]},
], label_key='id', on_select=lambda e: ui.notify(e.value))

tree.add_slot('default-header', r'''
    <div class="row items-center">
        <q-icon :name="props.node.icon || 'share'" color="orange" size="28px" class="q-mr-sm" />
        <div class="text-weight-bold text-primary">{{ props.node.id }}</div>
    </div>
''')

with tree.add_slot('default-body'):
    ui.label('This is some default content.').classes('ml-8 text-weight-light text-black')

ui.run()
