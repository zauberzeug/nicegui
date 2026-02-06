import asyncio
from typing import Literal

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import SharedScreen


def test_input(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.input('Your name', value='John Doe')

    shared_screen.open('/')
    shared_screen.should_contain('Your name')
    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Your name"]')
    assert element.get_attribute('type') == 'text'
    assert element.get_attribute('value') == 'John Doe'

    element.send_keys(' Jr.')
    assert element.get_attribute('value') == 'John Doe Jr.'


def test_password(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.input('Your password', value='123456', password=True)

    shared_screen.open('/')
    shared_screen.should_contain('Your password')

    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Your password"]')
    assert element.get_attribute('type') == 'password'
    assert element.get_attribute('value') == '123456'

    element.send_keys('789')
    shared_screen.wait(0.5)
    assert element.get_attribute('value') == '123456789'


def test_toggle_button(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.input('Your password', value='123456', password=True, password_toggle_button=True)

    shared_screen.open('/')
    shared_screen.should_contain('Your password')
    shared_screen.should_contain('visibility_off')

    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Your password"]')
    assert element.get_attribute('type') == 'password'
    assert element.get_attribute('value') == '123456'

    shared_screen.click('visibility_off')
    shared_screen.wait(0.5)
    assert element.get_attribute('type') == 'text'

    shared_screen.click('visibility')
    shared_screen.wait(0.5)
    assert element.get_attribute('type') == 'password'


@pytest.mark.parametrize('method', ['dict', 'sync', 'async'])
def test_input_validation(method: Literal['dict', 'sync', 'async'], shared_screen: SharedScreen):
    input_ = None

    @ui.page('/')
    def page():
        nonlocal input_
        if method == 'sync':
            input_ = ui.input('Name',
                              validation=lambda x: 'Short' if len(x) < 3 else 'Still short' if len(x) < 5 else None)
        elif method == 'dict':
            input_ = ui.input('Name',
                              validation={'Short': lambda x: len(x) >= 3, 'Still short': lambda x: len(x) >= 5})
        else:
            async def validate(x: str) -> str | None:
                await asyncio.sleep(0.1)
                return 'Short' if len(x) < 3 else 'Still short' if len(x) < 5 else None
            input_ = ui.input('Name', validation=validate)

    def assert_validation(expected: bool):
        if method == 'async':
            with pytest.raises(NotImplementedError):
                input_.validate()
            assert input_.validate(return_result=False)
        else:
            assert input_.validate() == expected

    shared_screen.open('/')
    shared_screen.should_contain('Name')

    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]')
    element.send_keys('Jo')
    shared_screen.should_contain('Short')
    assert input_.error == 'Short'
    assert_validation(False)

    element.send_keys('hn')
    shared_screen.should_contain('Still short')
    assert input_.error == 'Still short'
    assert_validation(False)

    element.send_keys(' Doe')
    shared_screen.wait(1.0)
    shared_screen.should_not_contain('Short')
    shared_screen.should_not_contain('Still short')
    assert input_.error is None
    assert_validation(True)


def test_input_with_multi_word_error_message(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        input_ = ui.input(label='some input')
        ui.button('set error', on_click=lambda: input_.props('error error-message="Some multi word error message"'))

    shared_screen.open('/')
    shared_screen.should_not_contain('Some multi word error message')

    shared_screen.click('set error')
    shared_screen.should_contain('Some multi word error message')


def test_autocompletion(shared_screen: SharedScreen):
    input_ = None

    @ui.page('/')
    def page():
        nonlocal input_
        input_ = ui.input('Input', autocomplete=['foo', 'bar', 'baz'])

    shared_screen.open('/')
    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Input"]')
    element.send_keys('f')
    shared_screen.should_contain('oo')

    element.send_keys('l')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('oo')

    element.send_keys(Keys.BACKSPACE)
    shared_screen.should_contain('oo')

    element.send_keys(Keys.TAB)
    shared_screen.wait(0.2)
    assert element.get_attribute('value') == 'foo'
    assert input_.value == 'foo'

    element.send_keys(Keys.BACKSPACE)
    element.send_keys(Keys.BACKSPACE)
    element.send_keys('x')
    element.send_keys(Keys.TAB)
    shared_screen.wait(0.5)
    assert element.get_attribute('value') == 'fx'
    assert input_.value == 'fx'

    input_.set_autocomplete(['once', 'twice'])
    shared_screen.wait(0.2)
    element.send_keys(Keys.BACKSPACE)
    element.send_keys(Keys.BACKSPACE)
    element.send_keys('o')
    shared_screen.should_contain('nce')


def test_clearable_input(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        input_ = ui.input(value='foo').props('clearable')
        ui.label().bind_text_from(input_, 'value', lambda value: f'value: {value}')

    shared_screen.open('/')
    shared_screen.should_contain('value: foo')
    shared_screen.click('cancel')
    shared_screen.should_contain('value: None')


def test_update_input(shared_screen: SharedScreen):
    input_ = None

    @ui.page('/')
    def page():
        nonlocal input_
        input_ = ui.input('Name', value='Pete')

    shared_screen.open('/')
    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]')
    assert element.get_attribute('value') == 'Pete'

    element.send_keys('r')
    shared_screen.wait(0.5)
    assert element.get_attribute('value') == 'Peter'

    input_.value = 'Pete'
    shared_screen.wait(0.5)
    assert element.get_attribute('value') == 'Pete'


def test_switching_focus(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        input1 = ui.input()
        input2 = ui.input()
        ui.button('focus 1', on_click=lambda: input1.run_method('focus'))
        ui.button('focus 2', on_click=lambda: input2.run_method('focus'))

    shared_screen.open('/')
    elements = shared_screen.selenium.find_elements(By.XPATH, '//input')
    assert len(elements) == 2
    shared_screen.click('focus 1')
    shared_screen.wait(0.3)
    assert elements[0] == shared_screen.selenium.switch_to.active_element
    shared_screen.click('focus 2')
    shared_screen.wait(0.3)
    assert elements[1] == shared_screen.selenium.switch_to.active_element


def test_prefix_and_suffix(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        n = ui.input(prefix='MyPrefix', suffix='MySuffix')

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
