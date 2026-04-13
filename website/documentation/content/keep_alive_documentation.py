from nicegui import ui

from . import doc


@doc.demo(ui.keep_alive)
def main_demo() -> None:
    with ui.tabs() as tabs:
        ui.tab('Other')
        ui.tab('Terminal')
    with ui.tab_panels(tabs, value='Other'):
        with ui.tab_panel('Other'):
            ui.label('Open the second tab to see the buffered output.')
        with ui.tab_panel('Terminal'):
            with ui.keep_alive():
                terminal = ui.xterm()

    ui.button('Write hello', on_click=lambda: terminal.writeln('Hello, NiceGUI!'))


@doc.demo('Reading data from a hidden AG Grid', '''
    Without `ui.keep_alive`, calling `get_client_data` on a `ui.aggrid` inside an unopened tab or closed dialog
    would silently return an empty list because the grid has not been mounted yet.
    Wrapping the grid in `ui.keep_alive` mounts it eagerly, so its API is reachable immediately.
''')
def aggrid_demo() -> None:
    with ui.dialog() as dialog:
        with ui.keep_alive():
            grid = ui.aggrid({
                'columnDefs': [{'field': 'name'}, {'field': 'age'}],
                'rowData': [{'name': 'Alice', 'age': 18}, {'name': 'Bob', 'age': 21}],
            })
        ui.button('Close', on_click=dialog.close)

    async def show_data():
        ui.notify(await grid.get_client_data())

    ui.button('Open dialog', on_click=dialog.open)
    ui.button('Read data', on_click=show_data)


doc.reference(ui.keep_alive)
