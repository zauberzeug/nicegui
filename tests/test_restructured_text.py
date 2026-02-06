from nicegui import ui
from nicegui.testing import SharedScreen


def test_restructured_text(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        rst = ui.restructured_text('This is **reStructuredText**')
        ui.button('Set new content', on_click=lambda: rst.set_content('New **content**'))

    shared_screen.open('/')
    element = shared_screen.find('This is')
    assert element.text == 'This is reStructuredText'
    assert element.get_attribute('innerHTML') == 'This is <strong>reStructuredText</strong>'

    shared_screen.click('Set new content')
    element = shared_screen.find('New')
    assert element.text == 'New content'
    assert element.get_attribute('innerHTML') == 'New <strong>content</strong>'
