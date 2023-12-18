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
    ui.json_editor({'content': {'json': json}},
                   on_select=lambda e: ui.notify(f'Select: {e}'),
                   on_change=lambda e: ui.notify(f'Change: {e}'))


@doc.demo('Run methods', '''
    You can run methods of the JSONEditor instance using the `run_editor_method` method.
    This demo shows how to expand and collapse all nodes and how to get the current data.
''')
def methods_demo() -> None:
    json = {
        'Name': 'Alice',
        'Age': 42,
        'Address': {
            'Street': 'Main Street',
            'City': 'Wonderland',
        },
    }
    editor = ui.json_editor({'content': {'json': json}})

    ui.button('Expand All', on_click=lambda: editor.run_editor_method('expand', 'path => true'))
    ui.button('Collapse All', on_click=lambda: editor.run_editor_method('expand', 'path => false'))

    async def get_data() -> None:
        data = await editor.run_editor_method('get')
        ui.notify(data)
    ui.button('Get Data', on_click=get_data)


doc.reference(ui.json_editor)
