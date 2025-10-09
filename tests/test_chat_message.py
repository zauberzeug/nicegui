import pytest
from html_sanitizer import Sanitizer
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen


def test_text_vs_html(screen: Screen):
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
        with pytest.raises(ValueError):
            ui.chat_message('80&euro;', text_html=True)

    screen.open('/')
    screen.should_contain('10&euro;')
    screen.should_contain('20€')
    screen.should_contain('30€')
    screen.should_contain('40€')
    screen.should_contain('50€')
    screen.should_contain('60EUR')
    screen.should_not_contain('70€')
    screen.should_not_contain('80€')


def test_newline(screen: Screen):
    @ui.page('/')
    def page():
        ui.chat_message('Hello\nNiceGUI!')

    screen.open('/')
    assert screen.find('Hello').find_element(By.TAG_NAME, 'br')


def test_slot(screen: Screen):
    @ui.page('/')
    def page():
        with ui.chat_message():
            ui.label('slot')

    screen.open('/')
    screen.should_contain('slot')
