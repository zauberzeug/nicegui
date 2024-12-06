from nicegui import ui, ElementFilter

from . import doc


@doc.demo(ui.aggrid)
def main_demo() -> None:
    grid = ui.aggrid({
        'defaultColDef': {'flex': 1},
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age'},
            {'headerName': 'Parent', 'field': 'parent', 'hide': True},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18, 'parent': 'David'},
            {'name': 'Bob', 'age': 21, 'parent': 'Eve'},
            {'name': 'Carol', 'age': 42, 'parent': 'Frank'},
        ],
        'rowSelection': 'multiple',
    }).classes('max-h-40')

    def update():
        grid.options['rowData'][0]['age'] += 1
        grid.update()

    ui.button('Update', on_click=update)
    ui.button('Select all', on_click=lambda: grid.run_grid_method('selectAll'))
    ui.button('Show parent', on_click=lambda: grid.run_grid_method('setColumnsVisible', ['parent'], True))


@doc.demo('Select AG Grid Rows', '''
    You can add checkboxes to grid cells to allow the user to select single or multiple rows.

    To retrieve the currently selected rows, use the `get_selected_rows` method.
    This method returns a list of rows as dictionaries.

    If `rowSelection` is set to `'single'` or to get the first selected row,
    you can also use the `get_selected_row` method.
    This method returns a single row as a dictionary or `None` if no row is selected.

    See the [AG Grid documentation](https://www.ag-grid.com/javascript-data-grid/row-selection/#example-single-row-selection) for more information.
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

    async def output_selected_rows():
        rows = await grid.get_selected_rows()
        if rows:
            for row in rows:
                ui.notify(f"{row['name']}, {row['age']}")
        else:
            ui.notify('No rows selected.')

    async def output_selected_row():
        row = await grid.get_selected_row()
        if row:
            ui.notify(f"{row['name']}, {row['age']}")
        else:
            ui.notify('No row selected!')

    ui.button('Output selected rows', on_click=output_selected_rows)
    ui.button('Output selected row', on_click=output_selected_row)


@doc.demo('Filter Rows using Mini Filters', '''
    You can add [mini filters](https://ag-grid.com/javascript-data-grid/filter-set-mini-filter/)
    to the header of each column to filter the rows.

    Note how the "agTextColumnFilter" matches individual characters, like "a" in "Alice" and "Carol",
    while the "agNumberColumnFilter" matches the entire number, like "18" and "21", but not "1".
''')
def aggrid_with_minifilters():
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
            {'headerName': 'Age', 'field': 'age', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol', 'age': 42},
        ],
    }).classes('max-h-40')


@doc.demo('AG Grid with Conditional Cell Formatting', '''
    This demo shows how to use [cellClassRules](https://www.ag-grid.com/javascript-grid-cell-styles/#cell-class-rules)
    to conditionally format cells based on their values.
''')
def aggrid_with_conditional_cell_formatting():
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age', 'cellClassRules': {
                'bg-red-300': 'x < 21',
                'bg-green-300': 'x >= 21',
            }},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol', 'age': 42},
        ],
    })


@doc.demo('Create Grid from Pandas DataFrame', '''
    You can create an AG Grid from a Pandas DataFrame using the `from_pandas` method.
    This method takes a Pandas DataFrame as input and returns an AG Grid.
''')
def aggrid_from_pandas():
    import pandas as pd

    df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    ui.aggrid.from_pandas(df).classes('max-h-40')


@doc.demo('Create Grid from Polars DataFrame', '''
    You can create an AG Grid from a Polars DataFrame using the `from_polars` method.
    This method takes a Polars DataFrame as input and returns an AG Grid.
''')
def aggrid_from_polars():
    import polars as pl

    df = pl.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    ui.aggrid.from_polars(df).classes('max-h-40')


@doc.demo('Render columns as HTML', '''
    You can render columns as HTML by passing a list of column indices to the `html_columns` argument.
''')
def aggrid_with_html_columns():
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'URL', 'field': 'url'},
        ],
        'rowData': [
            {'name': 'Google', 'url': '<a href="https://google.com">https://google.com</a>'},
            {'name': 'Facebook', 'url': '<a href="https://facebook.com">https://facebook.com</a>'},
        ],
    }, html_columns=[1])


@doc.demo('Respond to an AG Grid event', '''
    All AG Grid events are passed through to NiceGUI via the AG Grid global listener.
    These events can be subscribed to using the `.on()` method.
''')
def aggrid_respond_to_event():
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age'},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol', 'age': 42},
        ],
    }).on('cellClicked', lambda event: ui.notify(f'Cell value: {event.args["value"]}'))


@doc.demo('AG Grid with complex objects', '''
    You can use nested complex objects in AG Grid by separating the field names with a period.
    (This is the reason why keys in `rowData` are not allowed to contain periods.)
''')
def aggrid_with_complex_objects():
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'First name', 'field': 'name.first'},
            {'headerName': 'Last name', 'field': 'name.last'},
            {'headerName': 'Age', 'field': 'age'}
        ],
        'rowData': [
            {'name': {'first': 'Alice', 'last': 'Adams'}, 'age': 18},
            {'name': {'first': 'Bob', 'last': 'Brown'}, 'age': 21},
            {'name': {'first': 'Carol', 'last': 'Clark'}, 'age': 42},
        ],
    }).classes('max-h-40')


@doc.demo('AG Grid with dynamic row height', '''
    You can set the height of individual rows by passing a function to the `getRowHeight` argument.
''')
def aggrid_with_dynamic_row_height():
    ui.aggrid({
        'columnDefs': [{'field': 'name'}, {'field': 'age'}],
        'rowData': [
            {'name': 'Alice', 'age': '18'},
            {'name': 'Bob', 'age': '21'},
            {'name': 'Carol', 'age': '42'},
        ],
        ':getRowHeight': 'params => params.data.age > 35 ? 50 : 25',
    }).classes('max-h-40')


@doc.demo('Run row methods', '''
    You can run methods on individual rows by using the `run_row_method` method.
    This method takes the row ID, the method name and the method arguments as arguments.
    The row ID is either the row index (as a string) or the value of the `getRowId` function.

    The following demo shows how to use it to update cell values.
    Note that the row selection is preserved when the value is updated.
    This would not be the case if the grid was updated using the `update` method.
''')
def aggrid_run_row_method():
    grid = ui.aggrid({
        'columnDefs': [
            {'field': 'name', 'checkboxSelection': True},
            {'field': 'age'},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol', 'age': 42},
        ],
        ':getRowId': '(params) => params.data.name',
    })
    ui.button('Update',
              on_click=lambda: grid.run_row_method('Alice', 'setDataValue', 'age', 99))


@doc.demo('Filter return values', '''
    You can filter the return values of method calls by passing string that defines a JavaScript function.
    This demo runs the grid method "getDisplayedRowAtIndex" and returns the "data" property of the result.

    Note that requesting data from the client is only supported for page functions, not for the shared auto-index page.
''')
def aggrid_filter_return_values():
    # @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [{'field': 'name'}],
            'rowData': [{'name': 'Alice'}, {'name': 'Bob'}],
        })

        async def get_first_name() -> None:
            row = await grid.run_grid_method('g => g.getDisplayedRowAtIndex(0).data')
            ui.notify(row['name'])

        ui.button('Get First Name', on_click=get_first_name)
    page()  # HIDE


@doc.demo('Handle theme change', '''
    You can change the theme of the AG Grid by adding or removing classes.
    This demo shows how to change the theme using a switch.
''')
def aggrid_handle_theme_change():
    from nicegui import events

    grid = ui.aggrid({})

    def handle_theme_change(e: events.ValueChangeEventArguments):
        grid.classes(add='ag-theme-balham-dark' if e.value else 'ag-theme-balham',
                     remove='ag-theme-balham ag-theme-balham-dark')

    ui.switch('Dark', on_change=handle_theme_change)


doc.reference(ui.aggrid)
