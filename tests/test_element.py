from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.element import Element

from .screen import Screen


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
    assert Element._parse_props('href=http://192.168.42.100/') == {'href': 'http://192.168.42.100/'}


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


def test_remove_and_clear(screen: Screen):
    with ui.row() as row:
        ui.label('Label A')
        b = ui.label('Label B')
        ui.label('Label C')

    ui.button('Remove B', on_click=lambda: row.remove(b))
    ui.button('Remove 0', on_click=lambda: row.remove(0))
    ui.button('Clear', on_click=lambda: row.clear())

    screen.open('/')
    screen.should_contain('Label A')
    screen.should_contain('Label B')
    screen.should_contain('Label C')

    screen.click('Remove B')
    screen.should_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_contain('Label C')

    screen.click('Remove 0')
    screen.should_not_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_contain('Label C')

    screen.click('Clear')
    screen.should_not_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_not_contain('Label C')


def test_setting_visibility_in_timer(screen: Screen):
    '''reproduction of https://github.com/zauberzeug/nicegui/issues/206'''
    @ui.page('/')
    def page():
        label = ui.label('Some Label')
        ui.timer(1, lambda: label.set_visibility(False))

    screen.open('/')
    screen.wait(0.5)
    screen.should_not_contain('Some Label')
