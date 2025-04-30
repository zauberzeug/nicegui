from itertools import product
from typing import Dict, List

from nicegui import ui
from nicegui.elements.codemirror import find_python_index, get_cumulative_js_length
from nicegui.testing import Screen


def test_codemirror(screen: Screen):
    ui.codemirror('Line 1\nLine 2\nLine 3')

    screen.open('/')
    screen.should_contain('Line 2')


def test_supported_values(screen: Screen):
    values: Dict[str, List[str]] = {}

    @ui.page('/')
    def page():
        editor = ui.codemirror()

        async def fetch():
            values['languages'] = await editor.run_method('getLanguages')
            values['themes'] = await editor.run_method('getThemes')
            values['supported_themes'] = editor.supported_themes
            values['supported_languages'] = editor.supported_languages
            ui.label('Done')
        ui.button('Fetch', on_click=fetch)

    screen.open('/')
    screen.click('Fetch')
    screen.wait_for('Done')
    assert values['languages'] == values['supported_languages']
    assert values['themes'] == values['supported_themes']


def test_change_set():
    @ui.page('/')
    def page():
        editor = ui.codemirror()

        editor.value = ''
        editor._apply_change_set([0, 1], [['A']])
        assert editor.value == 'A'

        editor.value = ''
        editor._apply_change_set([0, 2], [['AB']])
        assert editor.value == 'AB'

        editor.value = 'X'
        editor._apply_change_set([1, 2], [['AB']])
        assert editor.value == 'AB'

        editor.value = 'X'
        editor._apply_change_set([1, -1], [])
        assert editor.value == 'X'

        editor.value = 'X'
        editor._apply_change_set([1, -1, 0, 1], [[], ['Y']])
        assert editor.value == 'XY'

        editor.value = 'Hello'
        editor._apply_change_set([5, -1, 0, 8], [[], [', world!']])
        assert editor.value == 'Hello, world!'

        editor.value = 'Hello, world!'
        editor._apply_change_set([5, -1, 7, 0, 1, -1], [])
        assert editor.value == 'Hello!'


def test_find_python_index():
    n = 10
    for combination in product([chr(20), chr(70000)], repeat=n):
        cumulative_js_length = get_cumulative_js_length(combination)
        for elem in cumulative_js_length:
            assert cumulative_js_length[find_python_index(elem, cumulative_js_length)-1] == elem, f"Failed for {elem}"
