from typing import List

from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_codemirror(screen: SeleniumScreen):
    ui.codemirror('Line 1\nLine 2\nLine 3')

    screen.open('/')
    screen.should_contain('Line 2')


def test_supported_values(screen: SeleniumScreen):
    values: dict[str, List[str]] = {}
    editor = ui.codemirror()

    async def fetch():
        values['languages'] = await editor.run_method('getLanguages')
        values['themes'] = await editor.run_method('getThemes')
        ui.label('Done')
    ui.button('Fetch', on_click=fetch)

    screen.open('/')
    screen.click('Fetch')
    screen.wait_for('Done')
    assert values['languages'] == editor.supported_languages
    assert values['themes'] == editor.supported_themes
