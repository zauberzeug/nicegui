from typing import Dict, List

from nicegui import ui
from nicegui.elements.codemirror import _apply_change_set
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
    assert _apply_change_set('', [0, 1], [['A']]) == 'A'
    assert _apply_change_set('', [0, 2], [['AB']]) == 'AB'
    assert _apply_change_set('X', [1, 2], [['AB']]) == 'AB'
    assert _apply_change_set('X', [1, -1], []) == 'X'
    assert _apply_change_set('X', [1, -1, 0, 1], [[], ['Y']]) == 'XY'
    assert _apply_change_set('Hello', [5, -1, 0, 8], [[], [', world!']]) == 'Hello, world!'
    assert _apply_change_set('Hello, world!', [5, -1, 7, 0, 1, -1], []) == 'Hello!'
    assert _apply_change_set('Hello, hello!', [2, -1, 3, 1, 4, -1, 3, 1, 1, -1], [[], ['y'], [], ['y']]) == 'Hey, hey!'
