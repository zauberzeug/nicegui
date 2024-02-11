
from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_editor(screen: SeleniumScreen):
    editor = ui.editor(placeholder='Type something here')
    ui.markdown().bind_content_from(editor, 'value', backward=lambda v: f'HTML code:\n```\n{v}\n```')

    screen.open('/')
    screen.find_by_class('q-editor__content').click()
    screen.type('Hello\nworld!')
    screen.wait(0.5)
    screen.should_contain('Hello<div>world!</div>')
