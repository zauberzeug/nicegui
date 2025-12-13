import pytest

from nicegui import ui
from nicegui.testing import Screen


def test_json_editor_methods(screen: Screen):
    @ui.page('/')
    def page():
        editor = ui.json_editor({'content': {'json': {'a': 1, 'b': 2}}})

        async def get_data():
            data = await editor.run_editor_method('get')
            ui.label(f'Data: {data}')
        ui.button('Get Data', on_click=get_data)

    screen.open('/')
    screen.should_contain('text')
    screen.should_contain('tree')
    screen.should_contain('table')

    screen.click('Get Data')
    screen.should_contain("Data: {'json': {'a': 1, 'b': 2}}")


def test_json_editor_validation(screen: Screen):
    @ui.page('/')
    def page():
        ui.json_editor({'content': {'json': {'x': 0}}},
                       schema={'type': 'object', 'properties': {'x': {'type': 'string'}}})

    screen.open('/')
    screen.should_contain('must be string')


@pytest.mark.parametrize('valid_uuid', [True, False])
def test_json_editor_validate_uuid(screen: Screen, valid_uuid: str):
    @ui.page('/')
    def page():
        schema = {
            'type': 'object',
            'properties': {
                'uuid': {
                    'type': 'string',
                    'format': 'uuid',
                },
            },
            'required': ['uuid'],
        }
        data = {
            'uuid': '123e4567-e89b-12d3-a456-426614174000' if valid_uuid else 'invalid-uuid',
        }
        ui.json_editor({'content': {'json': data}}, schema=schema)

    screen.open('/')
    if valid_uuid:
        screen.should_not_contain('must match format')
    else:
        screen.should_contain('must match format')
