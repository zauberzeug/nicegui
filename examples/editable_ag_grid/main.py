#!/usr/bin/env python3
from nicegui import ui


def add_row():
    new_id = max((dx['id'] for dx in aggrid.options['rowData']), default=-1) + 1
    aggrid.options['rowData'].append({'id': new_id, 'name': 'New name', 'age': None})
    ui.notify(f'Added row with ID {new_id}')


def handle_cell_value_change(e):
    new_row = e.args['data']
    ui.notify(f'Updated row to: {e.args["data"]}')
    aggrid.options['rowData'][:] = [row | new_row if row['id'] ==
                                    new_row['id'] else row for row in aggrid.options['rowData']]


async def delete_selected():
    selected_id = [row['id'] for row in await aggrid.get_selected_rows()]
    aggrid.options['rowData'][:] = [row for row in aggrid.options['rowData'] if row['id'] not in selected_id]
    ui.notify(f'Deleted row with ID {selected_id}')

aggrid = ui.aggrid({
    'columnDefs': [
        {'field': 'name', 'editable': True, 'sortable': True},
        {'field': 'age', 'editable': True},
        {'field': 'id'},
    ],
    'rowData': [
        {'id': 0, 'name': 'Alice', 'age': 18},
        {'id': 1, 'name': 'Bob', 'age': 21},
        {'id': 2, 'name': 'Carol', 'age': 20},
    ],
    'rowSelection': {'mode': 'multiRow'},
    'stopEditingWhenCellsLoseFocus': True,
}).on('cellValueChanged', handle_cell_value_change)

ui.button('Delete selected', on_click=delete_selected)
ui.button('New row', on_click=add_row)


ui.run()
