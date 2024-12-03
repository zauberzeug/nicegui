from typing import Optional

import pytest
from selenium.webdriver import Keys

from nicegui import ui
from nicegui.testing import Screen


def test_select(screen: Screen):
    ui.select(['A', 'B', 'C'], value='A')

    screen.open('/')
    screen.should_contain('A')
    screen.should_not_contain('B')
    screen.should_not_contain('C')

    screen.click('A')  # open the dropdown
    screen.click('B')  # close the dropdown
    screen.wait(0.5)
    screen.should_not_contain('A')
    screen.should_contain('B')
    screen.should_not_contain('C')


def test_select_with_input(screen: Screen):
    ui.select(['A', 'AB', 'XYZ'], with_input=True)

    screen.open('/')
    screen.find_by_tag('input').click()
    screen.should_contain('XYZ')

    screen.find_by_tag('input').send_keys('A')
    screen.wait(0.5)
    screen.should_contain('A')
    screen.should_contain('AB')
    screen.should_not_contain('XYZ')

    screen.find_by_tag('input').send_keys('ABC' + Keys.ENTER)
    screen.find_by_tag('input').click()
    screen.should_not_contain('ABC')


def test_replace_select(screen: Screen):
    with ui.row() as container:
        ui.select(['A'], value='A')

    def replace():
        container.clear()
        with container:
            ui.select(['B'], value='B')
    ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('A')
    screen.click('Replace')
    screen.should_contain('B')
    screen.should_not_contain('A')


def test_multi_select(screen: Screen):
    s = ui.select(['Alice', 'Bob', 'Carol'], value='Alice', multiple=True).props('use-chips')
    ui.label().bind_text_from(s, 'value', backward=str)

    screen.open('/')
    screen.should_contain("['Alice']")
    screen.click('Alice')
    screen.click('Bob')
    screen.should_contain("['Alice', 'Bob']")

    screen.click('cancel')  # remove icon
    screen.should_contain("['Bob']")


def test_changing_options(screen: Screen):
    s = ui.select([10, 20, 30], value=10)
    ui.label().bind_text_from(s, 'value', lambda v: f'value = {v}')
    ui.button('reverse', on_click=lambda: (s.options.reverse(), s.update()))
    ui.button('clear', on_click=lambda: (s.options.clear(), s.update()))

    screen.open('/')
    screen.click('reverse')
    screen.should_contain('value = 10')
    screen.click('clear')
    screen.should_contain('value = None')


def test_set_options(screen:  Screen):
    s = ui.select([1, 2, 3], value=1)
    ui.button('Set new options', on_click=lambda: s.set_options([4, 5, 6], value=4))

    screen.open('/')
    screen.click('Set new options')
    screen.click('4')
    screen.should_contain('5')
    screen.should_contain('6')


@pytest.mark.parametrize('option_dict', [False, True])
@pytest.mark.parametrize('multiple', [False, True])
@pytest.mark.parametrize('new_value_mode', ['add', 'add-unique', 'toggle', None])
def test_add_new_values(screen:  Screen, option_dict: bool, multiple: bool, new_value_mode: Optional[str]):
    options = {'a': 'A', 'b': 'B', 'c': 'C'} if option_dict else ['a', 'b', 'c']
    if option_dict and new_value_mode == 'add':
        with pytest.raises(ValueError, match='new_value_mode "add" is not supported for dict options'):
            ui.select(options=options, multiple=multiple, new_value_mode=new_value_mode)
        return

    s = ui.select(options=options, multiple=multiple, new_value_mode=new_value_mode)
    ui.label().bind_text_from(s, 'value', lambda v: f'value = {v}')
    ui.label().bind_text_from(s, 'options', lambda v: f'options = {v}')

    screen.open('/')
    screen.should_contain('value = []' if multiple else 'value = None')
    screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C'}" if option_dict else "options = ['a', 'b', 'c']")

    screen.find_by_class('q-select').click()
    screen.wait(0.5)
    screen.find_all('A' if option_dict else 'a')[-1].click()
    screen.should_contain("value = ['a']" if multiple else 'value = a')

    if new_value_mode:
        for _ in range(2):
            screen.find_by_tag('input').send_keys(Keys.BACKSPACE + 'd')
            screen.wait(0.5)
            screen.find_by_tag('input').click()
            screen.wait(0.5)
            screen.find_by_tag('input').send_keys(Keys.ENTER)
            screen.wait(0.5)
        if new_value_mode == 'add':
            screen.should_contain("value = ['a', 'd', 'd']" if multiple else 'value = d')
            screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'd', 'd': 'd'}" if option_dict else
                                  "options = ['a', 'b', 'c', 'd', 'd']")
        elif new_value_mode == 'add-unique':
            screen.should_contain("value = ['a', 'd', 'd']" if multiple else 'value = d')
            screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'd'}" if option_dict else
                                  "options = ['a', 'b', 'c', 'd']")
        elif new_value_mode == 'toggle':
            screen.should_contain("value = ['a']" if multiple else 'value = None')
            screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C'}" if option_dict else
                                  "options = ['a', 'b', 'c']")


def test_id_generator(screen: Screen):
    options = {'a': 'A', 'b': 'B', 'c': 'C'}
    select = ui.select(options, value='b', new_value_mode='add', key_generator=lambda _: len(options))
    ui.label().bind_text_from(select, 'options', lambda v: f'options = {v}')

    screen.open('/')
    screen.find_by_tag('input').send_keys(Keys.BACKSPACE + 'd')
    screen.wait(0.5)
    screen.find_by_tag('input').send_keys(Keys.ENTER)
    screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C', 3: 'd'}")


@pytest.mark.parametrize('multiple', [False, True])
def test_keep_filtered_options(multiple: bool, screen: Screen):
    ui.select(options=['A1', 'A2', 'B1', 'B2'], with_input=True, multiple=multiple)

    screen.open('/')
    screen.find_by_tag('input').click()
    screen.should_contain('A1')
    screen.should_contain('A2')
    screen.should_contain('B1')
    screen.should_contain('B2')

    screen.find_by_tag('input').send_keys('A')
    screen.wait(0.5)
    screen.should_contain('A1')
    screen.should_contain('A2')
    screen.should_not_contain('B1')
    screen.should_not_contain('B2')

    screen.click('A1')
    screen.wait(0.5)
    screen.find_by_tag('input').click()
    screen.should_contain('A1')
    screen.should_contain('A2')
    if multiple:
        screen.should_not_contain('B1')
        screen.should_not_contain('B2')
    else:
        screen.should_contain('B1')
        screen.should_contain('B2')


@pytest.mark.parametrize('auto_validation', [True, False])
def test_select_validation(auto_validation: bool, screen: Screen):
    select = ui.select(['A', 'BC', 'DEF'], value='A', validation={'Too long': lambda v: len(v) < 3})
    if not auto_validation:
        select.without_auto_validation()

    screen.open('/')
    screen.click('A')
    screen.click('DEF')
    screen.wait(0.5)
    if auto_validation:
        screen.should_contain('Too long')
    else:
        screen.should_not_contain('Too long')


def test_invalid_value(screen: Screen):
    with pytest.raises(ValueError, match='Invalid value: X'):
        ui.select(['A', 'B', 'C'], value='X')

    screen.open('/')
