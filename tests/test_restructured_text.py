from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_restructured_text(screen: SeleniumScreen):
    rst = ui.restructured_text('This is **reStructuredText**')

    screen.open('/')
    element = screen.find('This is')
    assert element.text == 'This is reStructuredText'
    assert element.get_attribute('innerHTML') == 'This is <strong>reStructuredText</strong>'

    rst.set_content('New **content**')
    element = screen.find('New')
    assert element.text == 'New content'
    assert element.get_attribute('innerHTML') == 'New <strong>content</strong>'
