from html_sanitizer import Sanitizer

from nicegui import html, ui
from nicegui.testing import SharedScreen


def test_html_element(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.html('This is strong.', sanitize=False, tag='strong')

    shared_screen.open('/')
    assert shared_screen.find_by_tag('strong').text == 'This is strong.'


def test_html_button(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        html.button('Click me').on('click', lambda: ui.notify('Hi!'))

    shared_screen.open('/')
    shared_screen.click('Click me')
    shared_screen.should_contain('Hi!')


def test_sanitize(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.html('<img src=x onerror=Quasar.Notify.create({message:"A"})>', sanitize=False)
        ui.html('<img src=x onerror=Quasar.Notify.create({message:"B"})>', sanitize=str)
        ui.html('<img src=x onerror=Quasar.Notify.create({message:"C"})>', sanitize=lambda x: x.replace('C', 'C!'))
        ui.html('<img src=x onerror=Quasar.Notify.create({message:"D"})>', sanitize=Sanitizer().sanitize)

    shared_screen.allowed_js_errors.append('/x - Failed to load resource')
    shared_screen.open('/')
    shared_screen.should_contain('A')
    shared_screen.should_contain('B')
    shared_screen.should_contain('C!')
    shared_screen.should_not_contain('D')


def test_xss_sanitization(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.html('<img src=x onerror="alert(\'XSS\')">')

    shared_screen.allowed_js_errors.append('/x - Failed to load resource')
    shared_screen.open('/')
    assert shared_screen.find_by_tag('img').get_attribute('onerror') is None
