from typing import Optional

import pytest
from selenium.webdriver import Keys

from nicegui import ui
from nicegui.testing import Screen


def test_input_chips(screen: Screen):
    with ui.row() as container:
        ui.input_chips('A')

    def replace():
        container.clear()
        with container:
            ui.input_chips('B')
    ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('A')
    screen.click('Replace')
    screen.should_contain('B')
    screen.should_not_contain('A')
    screen.click('cancel')  # remove icon
    screen.should_not_contain('A')
    screen.should_not_contain('B')


@pytest.mark.parametrize('new_value_mode', ['add', 'add-unique', 'toggle'])
def test_add_new_values(screen:  Screen, new_value_mode: str):

    s = ui.input_chips(new_value_mode=new_value_mode)
    ui.label().bind_text_from(s, 'value', lambda v: f'value = {v}')

    screen.open('/')
    screen.should_contain('value = []')

    screen.find_by_tag('input').send_keys('a' + Keys.ENTER)
    screen.wait(0.5)

    if new_value_mode:
        for _ in range(2):
            screen.find_by_tag('input').send_keys('d')
            screen.wait(0.5)
            screen.find_by_tag('input').click()
            screen.wait(0.5)
            screen.find_by_tag('input').send_keys(Keys.ENTER)
            screen.wait(0.5)
        if new_value_mode == 'add':
            screen.should_contain("value = ['a', 'd', 'd']")
        elif new_value_mode == 'add-unique':
            screen.should_contain("value = ['a', 'd']")
        elif new_value_mode == 'toggle':
            screen.should_contain("value = ['a']")

@pytest.mark.parametrize('auto_validation', [True, False])
def test_input_chips_validation(auto_validation: bool, screen: Screen):
    input_chips = ui.input_chips(['A', 'BC'], validation={'Too many': lambda v: len(v) < 3})
    if not auto_validation:
        input_chips.without_auto_validation()

    screen.open('/')
    screen.find_by_tag('input').send_keys('DEF')
    screen.wait(0.5)
    screen.find_by_tag('input').click()
    screen.wait(0.5)
    screen.find_by_tag('input').send_keys(Keys.ENTER)
    screen.wait(0.5)

    if auto_validation:
        screen.should_contain('Too many')
    else:
        screen.should_not_contain('Too many')
