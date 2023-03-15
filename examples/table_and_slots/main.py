#!/usr/bin/env python3
from nicegui import ui


class Demo:
    filter = ''
    fields = [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True},
        {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
    ]

    data = [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carol'},
    ]


with ui.qtable(title='QTable', columns=Demo.fields, rows=Demo.data, key='name', selection='single') \
        .bind_value(Demo, 'filter') as table:
    with table.add_slot('top-right'):
        with ui.input(placeholder='Search').props('type="search"').bind_value(Demo, 'filter') as search:
            with search.add_slot('append'):
                ui.icon('search')

    with table.add_slot('top-row'):
        with table.row():
            with table.cell().props('colspan="100%"'):
                ui.label('This is a top row').classes('text-center')

    with table.add_slot('bottom-row'):
        with table.row():
            with table.cell().props('colspan="100%"'):
                ui.label('This is a bottom row').classes('text-center')

    with table.add_slot('bottom'):
        ui.label('Bottom slot')

ui.label('').bind_text_from(table, 'selected', lambda val: f'Current selection: {val.__repr__()}')

ui.run()
