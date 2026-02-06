from nicegui import ui
from nicegui.testing import SharedScreen


def test_json_editor_methods(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        editor = ui.json_editor({'content': {'json': {'a': 1, 'b': 2}}})

        async def get_data():
            data = await editor.run_editor_method('get')
            ui.label(f'Data: {data}')
        ui.button('Get Data', on_click=get_data)

    shared_screen.open('/')
    shared_screen.should_contain('text')
    shared_screen.should_contain('tree')
    shared_screen.should_contain('table')

    shared_screen.click('Get Data')
    shared_screen.should_contain("Data: {'json': {'a': 1, 'b': 2}}")


def test_json_editor_validation(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.json_editor({'content': {'json': {'x': 0}}},
                       schema={'type': 'object', 'properties': {'x': {'type': 'string'}}})

    shared_screen.open('/')
    shared_screen.should_contain('must be string')


def test_json_editor_validate_uuid(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        editor = ui.json_editor({
            'content': {'json': {'id': '00000000-0000-0000-0000-000000000000'}},
        }, schema={
            'type': 'object',
            'properties': {
                'id': {'type': 'string', 'format': 'uuid'},
            },
            'required': ['id'],
        })
        ui.button('Replace ID', on_click=lambda: editor.properties['content']['json'].update(id='invalid-id'))

    shared_screen.open('/')
    shared_screen.should_contain('00000000-0000-0000-0000-000000000000')
    shared_screen.should_not_contain('must match format')

    shared_screen.click('Replace ID')
    shared_screen.should_contain('invalid-id')
    shared_screen.should_contain('must match format')
