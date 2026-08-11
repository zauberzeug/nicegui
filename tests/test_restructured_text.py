from pathlib import Path

from nicegui import ui
from nicegui.elements.restructured_text import prepare_content
from nicegui.testing import Screen


def test_restructured_text(screen: Screen):
    @ui.page('/')
    def page():
        rst = ui.restructured_text('This is **reStructuredText**')
        ui.button('Set new content', on_click=lambda: rst.set_content('New **content**'))

    screen.open('/')
    element = screen.find('This is')
    assert element.text == 'This is reStructuredText'
    assert element.get_attribute('innerHTML') == 'This is <strong>reStructuredText</strong>'

    screen.click('Set new content')
    element = screen.find('New')
    assert element.text == 'New content'
    assert element.get_attribute('innerHTML') == 'New <strong>content</strong>'


def test_file_insertion_directives_are_disabled(tmp_path: Path):
    secret = tmp_path / 'secret.txt'
    secret.write_text('TOP_SECRET_MARKER')
    for directive in [
        f'.. include:: {secret}',
        f'.. csv-table::\n   :file: {secret}',
        f'.. raw:: html\n   :file: {secret}',
    ]:
        assert 'TOP_SECRET_MARKER' not in prepare_content(directive)
