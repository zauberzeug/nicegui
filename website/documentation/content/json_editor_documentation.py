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

    The colon ":" in front of the method name "expand" indicates that the value "path => true" is a JavaScript expression
    that is evaluated on the client before it is passed to the method.

    Note that requesting data from the client is only supported for page functions, not for the shared auto-index page.
''')
def methods_demo() -> None:
    # @ui.page('/')
    def page():
        json = {
            'Name': 'Alice',
            'Age': 42,
            'Address': {
                'Street': 'Main Street',
                'City': 'Wonderland',
            },
        }
        editor = ui.json_editor({'content': {'json': json}})

        ui.button('Expand', on_click=lambda: editor.run_editor_method(':expand', 'path => true'))
        ui.button('Collapse', on_click=lambda: editor.run_editor_method(':expand', 'path => false'))
        ui.button('Readonly', on_click=lambda: editor.run_editor_method('updateProps', {'readOnly': True}))

        async def get_data() -> None:
            data = await editor.run_editor_method('get')
            ui.notify(data)
        ui.button('Get Data', on_click=get_data)
    page()  # HIDE


doc.reference(ui.json_editor)
