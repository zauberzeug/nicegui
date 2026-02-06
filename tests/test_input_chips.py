import pytest
from selenium.webdriver import Keys

from nicegui import ui
from nicegui.testing import SharedScreen


@pytest.mark.parametrize('new_value_mode', ['add', 'add-unique', 'toggle'])
def test_add_new_values(shared_screen: SharedScreen, new_value_mode: str):
    @ui.page('/')
    def page():
        chips = ui.input_chips(new_value_mode=new_value_mode)
        ui.label().bind_text_from(chips, 'value', lambda v: f'value = {v}')

    shared_screen.open('/')
    shared_screen.should_contain('value = []')

    shared_screen.find_by_tag('input').send_keys('x' + Keys.ENTER)
    shared_screen.wait(0.5)

    for _ in range(2):
        shared_screen.find_by_tag('input').send_keys('y' + Keys.ENTER)
        shared_screen.wait(0.5)

    if new_value_mode == 'add':
        shared_screen.should_contain("value = ['x', 'y', 'y']")
    elif new_value_mode == 'add-unique':
        shared_screen.should_contain("value = ['x', 'y']")
    elif new_value_mode == 'toggle':
        shared_screen.should_contain("value = ['x']")


@pytest.mark.parametrize('auto_validation', [True, False])
def test_input_chips_validation(auto_validation: bool, shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        input_chips = ui.input_chips(value=['A', 'BC'], validation={'Too many': lambda v: len(v) < 3})
        if not auto_validation:
            input_chips.without_auto_validation()

    shared_screen.open('/')
    shared_screen.find_by_tag('input').send_keys('DEF' + Keys.ENTER)
    shared_screen.wait(0.5)

    if auto_validation:
        shared_screen.should_contain('Too many')
    else:
        shared_screen.should_not_contain('Too many')
