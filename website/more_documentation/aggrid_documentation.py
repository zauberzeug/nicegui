from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    grid = ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age'},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol', 'age': 42},
        ],
        'rowSelection': 'multiple',
    }).classes('max-h-40')

    def update():
        grid.options['rowData'][0]['age'] += 1
        grid.update()

    ui.button('Update', on_click=update)
    ui.button('Select all', on_click=lambda: grid.call_api_method('selectAll'))


def more() -> None:
    @text_demo('Select AGgrid Rows', '''
        Selection checkboxes can be added to rows, allowing for retrieval of user selection.\n
        Note that the on click for the buttons receive the callable function (no parentheses) and that they are not lambda functions.\n
        See the [AGgrid documentation](https://www.ag-grid.com/javascript-data-grid/row-selection/#example-single-row-selection) for more information.
    ''')
    def aggrid_with_selectable_rows():
        grid = ui.aggrid({
            'columnDefs': [
                {'headerName': 'Name', 'field': 'name', 'checkboxSelection': True},
                {'headerName': 'Age', 'field': 'age'},
            ],
            'rowData': [
                {'name': 'Alice', 'age': 18},
                {'name': 'Bob', 'age': 21},
                {'name': 'Carol', 'age': 42},
            ],
            'rowSelection': 'multiple',
        }).classes('max-h-40')

        async def get_rows():
            # This function grabs all selected rows (use when rowSelection is multiple)

            # Obtain rows
            rows = await grid.get_selected_rows()

            # Check if empty
            if rows == []:
                ui.notify("None selected!")
                return

            # Process as desired
            for row in rows:
                row_name = row["name"]
                row_age = row["age"]
                ui.notify(f"{row_name}, {row_age}")

        async def get_row():
            # This function grabs the row you selected (use when rowSelection is single)

            # Obtain row
            row = await grid.get_selected_row()

            # Check if None
            if row is None:
                ui.notify("None selected!")
                return

            # Process as desired
            row_name = row["name"]
            row_age = row["age"]
            ui.notify(f"{row_name}, {row_age}")

        ui.button('Get Rows', on_click=get_rows)
        ui.button('Get Row', on_click=get_row)

        ui.run()
