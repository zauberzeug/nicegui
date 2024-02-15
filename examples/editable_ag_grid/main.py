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


def add_row():
    """
    Add a new row to the grid.

    This function adds a new row to the grid by generating a unique ID for the row and appending it to the `rows` list.
    The new row will have a default name of 'New name' and an age of None.

    Returns:
        None

    Example:
        >>> add_row()
        Added row with ID 1
    """
    new_id = max((dx['id'] for dx in rows), default=-1) + 1
    rows.append({'id': new_id, 'name': 'New name', 'age': None})
    ui.notify(f'Added row with ID {new_id}')
    aggrid.update()


def handle_cell_value_change(e):
    """
    Handle the event when a cell value changes in the grid.

    Args:
        e (Event): The event object containing the data of the changed cell.

    Returns:
        None

    Description:
        This function is called when a cell value changes in the grid. It updates the corresponding row in the `rows` list
        with the new data. The `e` parameter is an event object that contains the data of the changed cell. The `new_row`
        variable is extracted from the event object and represents the updated row data. The function then iterates over
        the `rows` list and replaces the old row with the updated row if their `id` values match.

    Example:
        Suppose we have a grid with the following rows:
        rows = [
            {'id': 1, 'name': 'John', 'age': 25},
            {'id': 2, 'name': 'Jane', 'age': 30},
            {'id': 3, 'name': 'Bob', 'age': 35}
        ]

        If the cell with `id` 2 is changed to {'id': 2, 'name': 'Alice', 'age': 28}, the `handle_cell_value_change` function
        will update the `rows` list as follows:
        rows = [
            {'id': 1, 'name': 'John', 'age': 25},
            {'id': 2, 'name': 'Alice', 'age': 28},
            {'id': 3, 'name': 'Bob', 'age': 35}
        ]
    """
    new_row = e.args['data']
    ui.notify(f'Updated row to: {e.args["data"]}')
    rows[:] = [row | new_row if row['id'] == new_row['id'] else row for row in rows]


async def delete_selected():
    """
    Deletes the selected rows from the AG Grid.

    This function retrieves the IDs of the selected rows using the `aggrid.get_selected_rows()` method.
    It then filters the `rows` list to remove the rows with matching IDs.
    Finally, it updates the AG Grid to reflect the changes and displays a notification with the deleted row IDs.

    Usage:
    - Call this function to delete the selected rows from the AG Grid.

    Example:
    ```
    await delete_selected()
    ```

    Note:
    - This function assumes the existence of the following variables:
        - `aggrid`: An instance of the AG Grid component.
        - `rows`: A list containing the data of all rows in the AG Grid.
        - `ui`: An instance of the UI component used to display notifications.
    """
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
