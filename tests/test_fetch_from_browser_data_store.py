from nicegui import app, json, ui
from nicegui.testing import Screen


def test_fetch_string_from_browser_data_store(screen: Screen):
    app.browser_data_store['test_string'] = 'This is a test string.'

    @ui.page('/')
    def main_page() -> None:
        ui.label(ui.context.client.fetch_string_from_browser_data_store('test_string'))

    screen.open('/')
    assert screen.find('This is a test string.'), \
        'First time around, string fetched from browser data store should be displayed.'
    assert screen.selenium.page_source.find('updateBrowserDataStore(String.raw`{}`)') == -1, \
        'First time around, we should update the browser data store.'

    screen.wait(2)  # Wait for the hashes of the browser data store to be updated

    screen.open('/')
    assert screen.find('This is a test string.'), \
        'After reloading, the string should still be displayed.'
    assert screen.selenium.page_source.find('updateBrowserDataStore(String.raw`{}`)') != -1, \
        'After reloading, we should not update the browser data store again.'


def test_fetch_list_from_browser_data_store(screen: Screen):
    def tree_assertations():
        # stolen from tests/test_tree.py
        screen.should_contain('numbers')
        screen.should_contain('letters')
        screen.should_not_contain('1')
        screen.should_not_contain('2')
        screen.should_not_contain('A')
        screen.should_not_contain('B')

        screen.find_by_class('q-icon').click()
        screen.wait(0.5)
        screen.should_contain('1')
        screen.should_contain('2')
    app.browser_data_store['test_list'] = json.dumps([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ])

    ui.tree(ui.context.client.fetch_list_from_browser_data_store('test_list'), label_key='id')

    # stolen from tests/test_tree.py
    screen.open('/')
    tree_assertations()
    assert screen.selenium.page_source.find('updateBrowserDataStore(String.raw`{}`)') == -1, \
        'First time around, we should update the browser data store.'

    screen.wait(2)  # Wait for the hashes of the browser data store to be updated

    screen.open('/')
    tree_assertations()
    assert screen.selenium.page_source.find('updateBrowserDataStore(String.raw`{}`)') != -1, \
        'After reloading, we should not update the browser data store again.'


def test_fetch_dict_from_browser_data_store(screen: Screen):
    def json_editor_assertations():
        # stolen from tests/test_json_editor.py
        screen.should_contain('text')
        screen.should_contain('tree')
        screen.should_contain('table')

        screen.click('Get Data')
        screen.should_contain("Data: {'json': {'a': 1, 'b': 2}}")
    app.browser_data_store['test_dict'] = json.dumps({'content': {'json': {'a': 1, 'b': 2}}})

    @ui.page('/')
    def page():
        editor = ui.json_editor(ui.context.client.fetch_dict_from_browser_data_store('test_dict'))

        async def get_data():
            data = await editor.run_editor_method('get')
            ui.label(f'Data: {data}')
        ui.button('Get Data', on_click=get_data)

    screen.open('/')
    json_editor_assertations()
    assert screen.selenium.page_source.find('updateBrowserDataStore(String.raw`{}`)') == -1, \
        'First time around, we should update the browser data store.'

    screen.wait(2)  # Wait for the hashes of the browser data store to be updated

    screen.open('/')
    json_editor_assertations()
    assert screen.selenium.page_source.find('updateBrowserDataStore(String.raw`{}`)') != -1, \
        'After reloading, we should not update the browser data store again.'
