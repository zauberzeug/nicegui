from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nicegui import ui

from .screen import Screen


def test_input(screen: Screen):
    ui.input('Your name', value='John Doe')

    screen.open('/')
    screen.should_contain('Your name')
    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Your name"]')
    assert element.get_attribute('type') == 'text'
    assert element.get_attribute('value') == 'John Doe'

    element.send_keys(' Jr.')
    assert element.get_attribute('value') == 'John Doe Jr.'


def test_password(screen: Screen):
    ui.input('Your password', value='123456', password=True)

    screen.open('/')
    screen.should_contain('Your password')

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Your password"]')
    assert element.get_attribute('type') == 'password'
    assert element.get_attribute('value') == '123456'

    element.send_keys('789')
    screen.wait(0.5)
    assert element.get_attribute('value') == '123456789'


def test_toggle_button(screen: Screen):
    ui.input('Your password', value='123456', password=True, password_toggle_button=True)

    screen.open('/')
    screen.should_contain('Your password')
    screen.should_contain('visibility_off')

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Your password"]')
    assert element.get_attribute('type') == 'password'
    assert element.get_attribute('value') == '123456'

    screen.click('visibility_off')
    screen.wait(0.5)
    assert element.get_attribute('type') == 'text'

    screen.click('visibility')
    screen.wait(0.5)
    assert element.get_attribute('type') == 'password'


def test_input_validation(screen: Screen):
    input = ui.input('Name', validation={'Too short': lambda value: len(value) >= 5})

    screen.open('/')
    screen.should_contain('Name')

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]')
    element.send_keys('John')
    screen.should_contain('Too short')
    assert input.error == 'Too short'

    element.send_keys(' Doe')
    screen.wait(0.5)
    screen.should_not_contain('Too short')
    assert input.error is None


def test_input_with_multi_word_error_message(screen: Screen):
    input = ui.input(label='some input')
    ui.button('set error', on_click=lambda: input.props('error error-message="Some multi word error message"'))

    screen.open('/')
    screen.should_not_contain('Some multi word error message')

    screen.click('set error')
    screen.should_contain('Some multi word error message')


def test_autocompletion(screen: Screen):
    input = ui.input('Input', autocomplete=['foo', 'bar', 'baz'])

    screen.open('/')
    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Input"]')
    element.send_keys('f')
    screen.should_contain('oo')

    element.send_keys('l')
    screen.wait(0.5)
    screen.should_not_contain('oo')

    element.send_keys(Keys.BACKSPACE)
    screen.should_contain('oo')

    element.send_keys(Keys.TAB)
    screen.wait(0.2)
    assert element.get_attribute('value') == 'foo'
    assert input.value == 'foo'

    element.send_keys(Keys.BACKSPACE)
    element.send_keys(Keys.BACKSPACE)
    element.send_keys('x')
    element.send_keys(Keys.TAB)
    screen.wait(0.5)
    assert element.get_attribute('value') == 'fx'
    assert input.value == 'fx'

    input.set_autocomplete(['one', 'two'])
    element.send_keys(Keys.BACKSPACE)
    element.send_keys(Keys.BACKSPACE)
    element.send_keys('o')
    screen.should_contain('ne')


def test_clearable_input(screen: Screen):
    input = ui.input(value='foo').props('clearable')
    ui.label().bind_text_from(input, 'value', lambda value: f'value: {value}')

    screen.open('/')
    screen.should_contain('value: foo')
    screen.click('cancel')
    screen.should_contain('value: None')


def test_update_input(screen: Screen):
    input = ui.input('Name', value='Pete')

    screen.open('/')
    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]')
    assert element.get_attribute('value') == 'Pete'

    element.send_keys('r')
    screen.wait(0.5)
    assert element.get_attribute('value') == 'Peter'

    input.value = 'Pete'
    screen.wait(0.5)
    assert element.get_attribute('value') == 'Pete'
