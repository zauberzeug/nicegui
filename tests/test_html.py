from nicegui import html, ui
from nicegui.testing import Screen


def test_html_element(screen: Screen):
    ui.html('This is strong.', tag='strong')

    screen.open('/')
    assert screen.find_by_tag('strong').text == 'This is strong.'


def test_html_button(screen: Screen):
    html.button('Click me').on('click', lambda: ui.notify('Hi!'))

    screen.open('/')
    screen.click('Click me')
    screen.should_contain('Hi!')
