from nicegui import ui

from .. import doc


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


@doc.demo('Update content', '''
    You can update the content of the JSONEditor by updating the `properties` property.
''')
def update_content():
    import random

    def update_number():
        editor.properties['content']['json'].update(number=random.randint(0, 100))

    editor = ui.json_editor({'content': {'json': {'number': 0}}})
    ui.button('Update number', on_click=update_number)


@doc.demo('Validation', '''
    You can use the `schema` parameter to define a [JSON schema](https://json-schema.org/) for validating the data being edited.
    In this demo, the editor will warn if the data does not match the schema:

    - `id` must be an integer
    - `name` must be a string
    - `price` must be a number greater than 0
    - `uuid` must be a valid UUID (requires NiceGUI version 3.5.0 or higher)

    *Added in version 2.8.0*

    *Updated in version 3.5.0: Added support for [ajv-formats](https://ajv.js.org/packages/ajv-formats.html)*
''')
def schema_demo() -> None:
    schema = {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'integer',
            },
            'name': {
                'type': 'string',
            },
            'price': {
                'type': 'number',
                'exclusiveMinimum': 0,
            },
            'uuid': {
                'type': 'string',
                'format': 'uuid',
            },
        },
        'required': ['id', 'name', 'price', 'uuid'],
    }
    data = {
        'id': 42,
        'name': 'Banana',
        'price': 15.0,
        'uuid': '123e4567-e89b-12d3-a456-426614174000',
    }
    ui.json_editor({'content': {'json': data}}, schema=schema)


@doc.demo('Run methods', '''
    You can run methods of the JSONEditor instance using the `run_editor_method` method.
    This demo shows how to expand and collapse all nodes and how to get the current data.

    The colon ":" in front of the method name "expand" indicates that the value "path => true" is a JavaScript expression
    that is evaluated on the client before it is passed to the method.
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

    ui.button('Expand', on_click=lambda: editor.run_editor_method(':expand', '[]', 'path => true'))
    ui.button('Collapse', on_click=lambda: editor.run_editor_method('collapse', []))
    ui.button('Readonly', on_click=lambda: editor.run_editor_method('updateProps', {'readOnly': True}))

    async def get_data() -> None:
        data = await editor.run_editor_method('get')
        ui.notify(data)
    ui.button('Get Data', on_click=get_data)


doc.reference(ui.json_editor)
