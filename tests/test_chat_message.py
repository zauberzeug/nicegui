from html_sanitizer import Sanitizer
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import SharedScreen


def test_text_vs_html(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.chat_message('10&euro;')
        ui.chat_message('20&euro;', text_html=True, sanitize=False)
        ui.chat_message('30&euro;', text_html=True, sanitize=Sanitizer().sanitize)
        ui.chat_message('<img src=x onerror=Quasar.Notify.create({message:"40&euro;"})>', text_html=True,
                        sanitize=False)
        ui.chat_message('<img src=x onerror=Quasar.Notify.create({message:"50&euro;"})>', text_html=True, sanitize=str)
        ui.chat_message('<img src=x onerror=Quasar.Notify.create({message:"60&euro;"})>', text_html=True,
                        sanitize=lambda x: x.replace('&euro;', 'EUR'))
        ui.chat_message('<img src=x onerror=Quasar.Notify.create({message:"70&euro;"})>', text_html=True,
                        sanitize=Sanitizer().sanitize)
        ui.chat_message('80&euro;', text_html=True)
        ui.chat_message('90&euro;', text_html=True, sanitize=False)

    shared_screen.allowed_js_errors.append('/x - Failed to load resource')
    shared_screen.open('/')
    shared_screen.should_contain('10&euro;')
    shared_screen.should_contain('20€')
    shared_screen.should_contain('30€')
    shared_screen.should_contain('40€')
    shared_screen.should_contain('50€')
    shared_screen.should_contain('60EUR')
    shared_screen.should_not_contain('70€')
    shared_screen.should_contain('80€')
    shared_screen.should_contain('90€')


def test_newline(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.chat_message('Hello\nNiceGUI!')

    shared_screen.open('/')
    assert shared_screen.find('Hello').find_element(By.TAG_NAME, 'br')


def test_slot(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.chat_message():
            ui.label('slot')

    shared_screen.open('/')
    shared_screen.should_contain('slot')


def test_xss_sanitization(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.chat_message('<img src=x onerror="alert(\'XSS\')">', text_html=True)

    shared_screen.allowed_js_errors.append('/x - Failed to load resource')
    shared_screen.open('/')
    assert shared_screen.find_by_tag('img').get_attribute('onerror') is None
