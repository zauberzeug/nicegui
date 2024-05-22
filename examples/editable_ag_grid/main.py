#!/usr/bin/env python3
from nicegui import ui

columns = [
    {'field': 'name', 'editable': True, 'sortable': True},
    {'field': 'age', 'editable': True},
    {'field': 'id'},
]
rows = [
    {'id': 0, 'name': 'Alice', 'age': 18},
    {'id': 1, 'name': 'Bob', 'age': 21},
    {'id': 2, 'name': 'Carol', 'age': 20},
]


@ui.page('/')
def page():
    def add_row():
        new_id = max((dx['id'] for dx in rows), default=-1) + 1
        rows.append({'id': new_id, 'name': 'New name', 'age': None})
        ui.notify(f'Added row with ID {new_id}')
        aggrid.update()

    def handle_cell_value_change(e):
        new_row = e.args['data']
        ui.notify(f'Updated row to: {e.args["data"]}')
        rows[:] = [row | new_row if row['id'] == new_row['id'] else row for row in rows]

    async def delete_selected():
        selected_id = [row['id'] for row in await aggrid.get_selected_rows()]
        rows[:] = [row for row in rows if row['id'] not in selected_id]
        ui.notify(f'Deleted row with ID {selected_id}')
        aggrid.update()

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    ui.button('Delete selected', on_click=delete_selected)
    ui.button('New row', on_click=add_row)


ui.run()
