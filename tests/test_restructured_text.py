from nicegui import ui
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
