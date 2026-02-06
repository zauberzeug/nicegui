import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import SharedScreen


def test_number_input(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.number('Number', value=42)
        ui.button('Button')

    shared_screen.open('/')
    shared_screen.should_contain_input('42')
    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys('00')
    shared_screen.click('Button')
    shared_screen.should_contain_input('4200')


def test_apply_format_on_blur(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.number('Number', format='%.4f', value=3.14159)
        ui.button('Button')

    shared_screen.open('/')
    shared_screen.should_contain_input('3.1416')

    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys('789')
    shared_screen.click('Button')
    shared_screen.should_contain_input('3.1417')

    element.click()
    element.send_keys(Keys.BACKSPACE * 10 + '2')
    shared_screen.click('Button')
    shared_screen.should_contain_input('2.0000')


def test_max_value(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.number('Number', min=0, max=10, value=5)
        ui.button('Button')

    shared_screen.open('/')
    shared_screen.should_contain_input('5')

    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys('6')
    shared_screen.click('Button')
    shared_screen.should_contain_input('10')


def test_clearable_number(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        number = ui.number(value=42).props('clearable')
        ui.label().bind_text_from(number, 'value', lambda value: f'value: {value}')

    shared_screen.open('/')
    shared_screen.should_contain('value: 42')
    shared_screen.click('cancel')
    shared_screen.should_contain('value: None')
    shared_screen.click('value: None')  # loose focus
    shared_screen.wait(0.5)
    shared_screen.should_contain('value: None')


def test_out_of_limits(shared_screen: SharedScreen):
    number = None

    @ui.page('/')
    def page():
        nonlocal number
        number = ui.number('Number', min=0, max=10, value=5)
        ui.label().bind_text_from(number, 'out_of_limits', lambda value: f'out_of_limits: {value}')

    shared_screen.open('/')
    shared_screen.should_contain('out_of_limits: False')

    number.value = 11
    shared_screen.should_contain('out_of_limits: True')

    number.max = 15
    shared_screen.should_contain('out_of_limits: False')


@pytest.mark.parametrize('precision', [None, 1, -1])
def test_rounding(precision: int, shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        number = ui.number('Number', value=12, precision=precision)
        ui.label().bind_text_from(number, 'value', lambda value: f'number=_{value}_')

    shared_screen.open('/')
    shared_screen.should_contain('number=_12_')

    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys('.345')
    shared_screen.click('number=')  # blur the number input
    if precision is None:
        shared_screen.should_contain('number=_12.345_')
    elif precision == 1:
        shared_screen.should_contain('number=_12.3_')
    elif precision == -1:
        shared_screen.should_contain('number=_10.0_')


def test_int_float_conversion_on_error1(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.number('Number', validation={'Error': lambda value: value == 1}, value=1)

    shared_screen.open('/')
    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys('2')
    shared_screen.should_contain('Error')
    assert element.get_attribute('value') == '12'


def test_int_float_conversion_on_error2(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.number('Number', validation={'Error': lambda value: value == 1.02}, value=1.02)

    shared_screen.open('/')
    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys(Keys.BACKSPACE)
    shared_screen.should_contain('Error')
    assert element.get_attribute('value') == '1.0'


def test_changing_limits(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        number = ui.number('Number', max=0, value=0)
        ui.button('Raise max', on_click=lambda: setattr(number, 'max', 1))
        ui.button('Step up', on_click=lambda: number.run_method('(e) => e.getNativeElement().stepUp()'))

    shared_screen.open('/')
    shared_screen.should_contain_input('0')

    shared_screen.click('Step up')
    shared_screen.should_contain_input('0')

    shared_screen.click('Raise max')
    shared_screen.should_contain_input('0')

    shared_screen.click('Step up')
    shared_screen.should_contain_input('1')


def test_none_values(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        n = ui.number('Number', on_change=lambda e: ui.label(f'event: {e.value}'))
        ui.label().bind_text_from(n, 'value', lambda value: f'model: {value}')

    shared_screen.open('/')
    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Number"]')
    element.send_keys('0')
    shared_screen.should_contain_input('0')
    shared_screen.should_contain('model: 0')
    shared_screen.should_contain('event: 0')

    element.send_keys(Keys.BACKSPACE)
    shared_screen.should_contain_input('')
    shared_screen.should_contain('model: None')
    shared_screen.should_contain('event: None')

    element.send_keys('1')
    shared_screen.should_contain_input('1')
    shared_screen.should_contain('model: 1')
    shared_screen.should_contain('event: 1')


def test_prefix_and_suffix(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        n = ui.number(prefix='MyPrefix', suffix='MySuffix')

        def change_prefix_suffix():
            n.prefix = 'NewPrefix'
            n.suffix = 'NewSuffix'

        ui.button('Change', on_click=change_prefix_suffix)

    shared_screen.open('/')
    shared_screen.should_contain('MyPrefix')
    shared_screen.should_contain('MySuffix')

    shared_screen.click('Change')
    shared_screen.should_contain('NewPrefix')
    shared_screen.should_contain('NewSuffix')
