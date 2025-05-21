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
    ui.json_editor({'content': {'json': {'x': 0}}}, schema={'type': 'object', 'properties': {'x': {'type': 'string'}}})

    screen.open('/')
    screen.should_contain('must be string')
