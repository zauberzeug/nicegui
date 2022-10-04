
import pytest
from nicegui import ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from .screen import Screen


def test_keyboard(screen: Screen):
    result = ui.label()
    ui.keyboard(on_key=lambda e: result.set_text(f'{e.key, e.action}'))

    screen.open('/')
    assert screen.selenium.find_element(By.TAG_NAME, 'base')
    assert any(s.endswith('keyboard.js') for s in screen.get_attributes('script', 'src'))

    assert screen.selenium.find_element(By.XPATH, '//span[@data-nicegui="keyboard"]')
    ActionChains(screen.selenium).send_keys('t').perform()
    screen.should_contain('t, KeyboardAction(keydown=False, keyup=True, repeat=False)')


def test_joystick(screen: Screen):
    ui.joystick()

    screen.open('/')
    assert any(s.endswith('keyboard.js') for s in screen.get_attributes('script', 'src'))
    assert screen.selenium.find_element(By.XPATH, '//div[@data-nicegui="joystick"]')


@pytest.mark.skip(reason='not jet fixed; see https://github.com/zauberzeug/nicegui/issues/98')
def test_input_with_multi_word_error_message(screen: Screen):
    input = ui.input(label='some input')
    ui.button('set error', on_click=lambda: input.props('error-message="Some multi word error message" error=error'))

    screen.open('/')
    screen.should_not_contain('Some multi word error message')
    screen.click('set error')
    screen.should_contain('Some multi word error message')


def test_classes(screen: Screen):
    label = ui.label('Some label')

    def assert_classes(classes: str) -> None:
        assert screen.selenium.find_element(By.XPATH,
                                            f'//*[normalize-space(@class)="{classes}" and text()="Some label"]')

    screen.open('/')
    assert_classes('')

    label.classes('one')
    assert_classes('one')

    label.classes('one')
    assert_classes('one')

    label.classes('two three')
    assert_classes('one two three')

    label.classes(remove='two')
    assert_classes('one three')

    label.classes(replace='four')
    assert_classes('four')


def test_style(screen: Screen):
    label = ui.label('Some label')

    def assert_style(style: str) -> None:
        assert screen.selenium.find_element(By.XPATH, f'//*[normalize-space(@style)="{style}" and text()="Some label"]')

    screen.open('/')
    assert_style('')

    label.style('color: red')
    assert_style('color: red;')

    label.style('color: red')
    assert_style('color: red;')

    label.style('color: blue')
    assert_style('color: blue;')

    label.style('font-weight: bold')
    assert_style('color: blue; font-weight: bold;')

    label.style(remove='color: blue')
    assert_style('font-weight: bold;')

    label.style(replace='text-decoration: underline')
    assert_style('text-decoration: underline;')

    label.style('color: blue;')
    assert_style('text-decoration: underline; color: blue;')


def test_props(screen: Screen):
    input = ui.input()

    def assert_props(*props: str) -> None:
        class_conditions = [f'contains(@class, "q-field--{prop}")' for prop in props]
        assert screen.selenium.find_element(By.XPATH, f'//label[{" and ".join(class_conditions)}]')

    screen.open('/')
    assert_props('standard', 'labeled')

    input.props('dark')
    assert_props('standard', 'labeled', 'dark')

    input.props('dark')
    assert_props('standard', 'labeled', 'dark')

    input.props(remove='dark')
    assert_props('standard', 'labeled')
