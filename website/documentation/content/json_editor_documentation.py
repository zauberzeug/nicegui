from typing import Any, Dict

from nicegui import ui

from . import doc


@doc.demo(ui.json_editor)
def main_demo() -> None:
    json = {
        'array': [1, 2, 3],
        'boolean': True,
        'color': '#82b92c',
        None: None,
        'number': 123,
        'object': {
            'a': 'b',
            'c': 'd',
        },
        'time': 1575599819000,
        'string': 'Hello World',
    }
    editor = ui.json_editor({'content': {'json': json}},
                            on_select=lambda e: ui.notify(f'Select: {e}'),
                            on_change=lambda e: ui.notify(f'Change: {e}'))
    ui.button('Expand All', on_click=lambda: editor.run_api_method('expand', 'path => true'))
    ui.button('Collapse All', on_click=lambda: editor.run_api_method('expand', 'path => false'))

    async def show_data() -> None:
        data = await editor.run_api_method('get')
        ui.notify(data)
    ui.button('Show Data', on_click=show_data)


doc.reference(ui.json_editor)
