from html_sanitizer import Sanitizer

from nicegui import html, ui
from nicegui.testing import Screen


def test_html_element(screen: Screen):
    @ui.page('/')
    def page():
        ui.html('This is strong.', sanitize=False, tag='strong')

    screen.open('/')
    assert screen.find_by_tag('strong').text == 'This is strong.'


def test_html_button(screen: Screen):
    @ui.page('/')
    def page():
        html.button('Click me').on('click', lambda: ui.notify('Hi!'))

    screen.open('/')
    screen.click('Click me')
    screen.should_contain('Hi!')


def test_sanitize(screen: Screen):
    @ui.page('/')
    def page():
        ui.html('<img src=x onerror=Quasar.Notify.create({message:"A"})>', sanitize=False)
        ui.html('<img src=x onerror=Quasar.Notify.create({message:"B"})>', sanitize=str)
        ui.html('<img src=x onerror=Quasar.Notify.create({message:"C"})>', sanitize=lambda x: x.replace('C', 'C!'))
        ui.html('<img src=x onerror=Quasar.Notify.create({message:"D"})>', sanitize=Sanitizer().sanitize)

    screen.open('/')
    screen.should_contain('A')
    screen.should_contain('B')
    screen.should_contain('C!')
    screen.should_not_contain('D')
