
from nicegui import ui
from nicegui.elements.element import Element
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
    ui.joystick(on_move=lambda e: coordinates.set_text(f'move {e.data.vector.x:.3f}, {e.data.vector.y:.3f}'),
                on_end=lambda e: coordinates.set_text('end 0, 0'))
    coordinates = ui.label('start 0, 0')

    screen.open('/')
    assert any(s.endswith('keyboard.js') for s in screen.get_attributes('script', 'src'))
    joystick = screen.selenium.find_element(By.XPATH, '//div[@data-nicegui="joystick"]')
    assert joystick
    screen.should_contain('start 0, 0')
    ActionChains(screen.selenium).move_to_element_with_offset(joystick, 25, 25)\
        .click_and_hold().pause(1).move_by_offset(20, 20).pause(1).perform()
    screen.should_contain('move 0.400, -0.400')
    ActionChains(screen.selenium).move_to_element_with_offset(joystick, 25, 25).click().perform()
    screen.should_contain('end 0, 0')


def test_styling_joystick(screen: Screen):
    ui.joystick().style('background-color: gray;').classes('shadow-lg')

    screen.open('/')
    joystick = screen.selenium.find_element(By.XPATH, '//div[@data-nicegui="joystick"]')
    assert 'background-color: gray;' in joystick.get_attribute('style')
    assert 'shadow-lg' in joystick.get_attribute('class')


def test_input_with_multi_word_error_message(screen: Screen):
    input = ui.input(label='some input')
    ui.button('set error', on_click=lambda: input.props('error error-message="Some multi word error message"'))

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


def test_style_parsing():
    assert Element._parse_style('color: red; background-color: green') == {'color': 'red', 'background-color': 'green'}
    assert Element._parse_style('width:12em;height:34.5em') == {'width': '12em', 'height': '34.5em'}
    assert Element._parse_style('transform: translate(120.0px, 50%)') == {'transform': 'translate(120.0px, 50%)'}
    assert Element._parse_style('box-shadow: 0 0 0.5em #1976d2') == {'box-shadow': '0 0 0.5em #1976d2'}


def test_props_parsing():
    assert Element._parse_props('one two=1 three="abc def"') == {'one': True, 'two': '1', 'three': 'abc def'}
    assert Element._parse_props('loading percentage=12.5') == {'loading': True, 'percentage': '12.5'}
    assert Element._parse_props('size=50%') == {'size': '50%'}


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
