from nicegui import ui

from .user import User


def test_classes(user: User):
    label = ui.label('label')
    user.open('/')

    def assert_classes(classes: str) -> None:
        for i in range(20):
            if user.find('label').get_attribute('class') == classes:
                return
            user.sleep(0.01)
        else:
            raise AssertionError(f'Expected {classes}, got {user.find("label").get_attribute("class")}')

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


def test_style(user: User):
    label = ui.label('label')

    def style() -> str:
        user.open('/')
        return user.find('label').get_attribute('style')

    assert style() == ''

    label.style('color: red')
    assert style() == 'color: red;'

    label.style('color: red')
    assert style() == 'color: red;'

    label.style('color: blue')
    assert style() == 'color: blue;'

    label.style('font-weight: bold')
    assert style() == 'color: blue; font-weight: bold;'

    label.style(remove='color: blue')
    assert style() == 'font-weight: bold;'

    label.style(replace='text-decoration: underline')
    assert style() == 'text-decoration: underline;'


def test_props(user: User):
    input = ui.input('input')

    def props() -> str:
        user.open('/')
        element = user.selenium.find_element_by_tag_name('label')
        return [c.replace('q-field--', '') for c in element.get_attribute('class').split() if c.startswith('q-field--')]

    assert props() == ['standard', 'labeled']

    input.props('dark')
    assert props() == ['standard', 'labeled', 'dark']

    input.props('dark')
    assert props() == ['standard', 'labeled', 'dark']

    input.props(remove='dark')
    assert props() == ['standard', 'labeled']
