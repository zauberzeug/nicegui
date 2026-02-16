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

    screen.allowed_js_errors.append('/x - Failed to load resource')
    screen.open('/')
    screen.should_contain('A')
    screen.should_contain('B')
    screen.should_contain('C!')
    screen.should_not_contain('D')


def test_xss_sanitization(screen: Screen):
    @ui.page('/')
    def page():
        ui.html('<img src=x onerror="alert(\'XSS\')">')

    screen.allowed_js_errors.append('/x - Failed to load resource')
    screen.open('/')
    assert screen.find_by_tag('img').get_attribute('onerror') is None


def test_html_manipulation(screen: Screen):
    @ui.page('/')
    def page():
        html_element = ui.html('Old HTML')
        ui.button('1. Manipulate HTML', on_click=lambda: ui.run_javascript(f'''
            getHtmlElement({html_element.id}).innerHTML = "New HTML";
        '''))
        label = ui.label('Hi')
        ui.button('2. Manipulate Label', on_click=lambda: label.set_text('Ho'))

    screen.open('/')
    screen.click('1. Manipulate HTML')
    screen.should_contain('New HTML')
    screen.click('2. Manipulate Label')
    screen.should_contain('Ho')
    screen.should_not_contain('Old HTML')
