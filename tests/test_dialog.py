from typing import Callable

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen


def test_open_close_dialog(screen: Screen):
    @ui.page('/')
    def page():
        with ui.dialog() as d, ui.card():
            ui.label('Content')
            ui.button('Close', on_click=d.close)
        ui.button('Open', on_click=d.open)

    screen.open('/')
    screen.should_not_contain('Content')

    screen.click('Open')
    screen.wait(0.5)
    screen.should_contain('Content')

    screen.click('Close')
    screen.wait(0.5)
    screen.should_not_contain('Content')


def test_await_dialog(screen: Screen):
    @ui.page('/')
    def page():
        with ui.dialog() as dialog, ui.card():
            ui.button('Yes', on_click=lambda: dialog.submit('Yes'))
            ui.button('No', on_click=lambda: dialog.submit('No'))

        async def show() -> None:
            ui.notify(f'Result: {await dialog}')

        ui.button('Open', on_click=show)

    screen.open('/')
    screen.click('Open')
    screen.wait(0.2)
    screen.click('Yes')
    screen.should_contain('Result: Yes')

    screen.click('Open')
    screen.wait(0.2)
    screen.click('No')
    screen.should_contain('Result: No')

    screen.click('Open')
    screen.type(Keys.ESCAPE)
    screen.should_contain('Result: None')


def test_dialog_scroll_behavior(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_css('html { scroll-behavior: smooth }')
        ui.link('Go to bottom', '#bottom')
        ui.link_target('bottom').classes('mt-[2000px]')
        ui.button('dialog', on_click=lambda: ui.dialog(value=True))

    screen.open('/')
    screen.click('Go to bottom')
    screen.wait(1)
    position = screen.selenium.execute_script('return window.scrollY')
    assert position > 1000

    screen.click('dialog')
    screen.wait(0.5)
    screen.type(Keys.ESCAPE)
    screen.wait(0.2)
    assert screen.selenium.execute_script('return window.scrollY') == position


def test_dialog_in_menu(screen: Screen):
    @ui.page('/')
    def page():
        def create_dialog():
            with ui.dialog(value=True), ui.card():
                ui.label('Dialog content')
                ui.button('Delete menu', on_click=menu.delete)

        with ui.button('Open menu'):
            with ui.menu() as menu:
                ui.menu_item('Create dialog', on_click=create_dialog)

    screen.open('/')
    screen.click('Open menu')
    screen.click('Create dialog')
    screen.should_contain('Dialog content')  # even though the dialog is nested inside a hidden menu

    screen.click('Delete menu')
    screen.wait(0.5)
    screen.should_not_contain('Dialog content')  # it has been deleted together with the menu


@pytest.mark.parametrize('element_factory,selector,text', [
    (lambda: ui.input('Input'), '//*[@aria-label="Input"]', 'input'),
    (lambda: ui.textarea('Textarea'), '//*[@aria-label="Textarea"]', 'textarea'),
    (lambda: ui.color_input('Color'), '//*[@aria-label="Color"]', '#ff0000'),
    (lambda: ui.date_input('Date'), '//*[@aria-label="Date"]', '2025-12-31'),
    (lambda: ui.time_input('Time'), '//*[@aria-label="Time"]', '12:34'),
    (lambda: ui.number('Number'), '//*[@aria-label="Number"]', '42'),
    (ui.editor, '//*[contains(@class, "q-editor__content")]', 'editor'),
    (ui.codemirror, '//*[contains(@class, "cm-content")]', 'codemirror'),
])
def test_reopening_dialog_with_various_inputs(element_factory: Callable, selector: str, text: str, screen: Screen):
    @ui.page('/')
    def page():
        with ui.dialog(value=True) as dialog, ui.card():
            element_factory()
            ui.button('Close', on_click=dialog.close)
        ui.label().bind_text_from(dialog, 'value', lambda x: 'Dialog open' if x else 'Dialog closed')
        ui.button('Edit', on_click=dialog.open)

    screen.open('/')
    element = screen.selenium.find_element(By.XPATH, selector)
    element.click()
    element.send_keys(text)

    screen.click('Close')
    screen.should_contain('Dialog closed')

    screen.click('Edit')
    screen.should_contain('Dialog open')

    element = screen.selenium.find_element(By.XPATH, selector)
    actual = element.get_attribute('value') or element.text
    assert actual == text, f'Value of {selector} did not persist: expected {text!r}, got {actual!r}'
