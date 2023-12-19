import pytest
from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen


def test_number_input(screen: Screen):
    ui.number('Number')
    ui.button('Button')

    screen.open('/')
    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys('42')
    screen.click('Button')
    screen.should_contain_input('42')


def test_apply_format_on_blur(screen: Screen):
    ui.number('Number', format='%.4f', value=3.14159)
    ui.button('Button')

    screen.open('/')
    screen.should_contain_input('3.1416')

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys('789')
    screen.click('Button')
    screen.should_contain_input('3.1417')


def test_max_value(screen: Screen):
    ui.number('Number', min=0, max=10, value=5)
    ui.button('Button')

    screen.open('/')
    screen.should_contain_input('5')

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys('6')
    screen.click('Button')
    screen.should_contain_input('10')


def test_clearable_number(screen: Screen):
    number = ui.number(value=42).props('clearable')
    ui.label().bind_text_from(number, 'value', lambda value: f'value: {value}')

    screen.open('/')
    screen.should_contain('value: 42')
    screen.click('cancel')
    screen.should_contain('value: None')
    screen.click('value: None')  # loose focus
    screen.wait(0.5)
    screen.should_contain('value: None')


def test_out_of_limits(screen: Screen):
    number = ui.number('Number', min=0, max=10, value=5)
    ui.label().bind_text_from(number, 'out_of_limits', lambda value: f'out_of_limits: {value}')

    screen.open('/')
    screen.should_contain('out_of_limits: False')

    number.value = 11
    screen.should_contain('out_of_limits: True')

    number.max = 15
    screen.should_contain('out_of_limits: False')


@pytest.mark.parametrize('precision', [None, 1, -1])
def test_rounding(precision: int, screen: Screen):
    number = ui.number('Number', value=12, precision=precision)
    ui.label().bind_text_from(number, 'value', lambda value: f'number=_{value}_')

    screen.open('/')
    screen.should_contain('number=_12_')

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys('.345')
    screen.click('number=')  # blur the number input
    if precision is None:
        screen.should_contain('number=_12.345_')
    elif precision == 1:
        screen.should_contain('number=_12.3_')
    elif precision == -1:
        screen.should_contain('number=_10.0_')
