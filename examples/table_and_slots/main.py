#!/usr/bin/env python3
from nicegui import ui

fields = [
    {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True},
    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
]

rows = [
    {'id': 0, 'name': 'Alice', 'age': 18},
    {'id': 1, 'name': 'Bob', 'age': 21},
    {'id': 2, 'name': 'Lionel', 'age': 19},
    {'id': 3, 'name': 'Michael', 'age': 32},
    {'id': 4, 'name': 'Julie', 'age': 12},
    {'id': 5, 'name': 'Livia', 'age': 25},
    {'id': 6, 'name': 'Carol'},
]

def add_row(item):
    rows.append(item)
    table.update()

def remove_row(keys):
    for i in range(len(rows)):
        if rows[i]['id'] in keys:
            del rows[i]
            table.update()

with ui.qtable(title='QTable', columns=fields, rows=rows, key='id', selection='single', pagination=15) as table:
    with table.add_slot('top-right'):
        with ui.input(placeholder='Search').props('type="search"').bind_value(table, 'filter') as search:
            with search.add_slot('append'):
                ui.icon('search')

    with table.add_slot('top-row'):
        with table.row():
            with table.cell().props('colspan="100%"'):
                ui.label('This is a top row').classes('text-center')

    with table.add_slot('bottom-row'):
        with table.row():
            with table.cell().props('colspan="2"'):
                new_name = ui.input()
            with table.cell():
                ui.button('add row', on_click=lambda: add_row({'id': len(rows), 'name': new_name.value, 'age': 10}))

ui.label('').bind_text_from(table, 'selected', lambda val: f'Current selection: {val.__repr__()}')
ui.button('Remove selection', on_click=lambda: remove_row(table.selected['keys'])).bind_visibility(table, 'selected')

ui.run()
