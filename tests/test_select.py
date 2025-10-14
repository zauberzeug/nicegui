from typing import Literal, Optional

import pytest
from selenium.webdriver import Keys

from nicegui import ui
from nicegui.testing import Screen, User


def test_select(screen: Screen):
    options = [ui.as_option(val=v) for v in ('A', 'B', 'C')]

    @ui.page('/')
    def page():
        ui.select(options, selected=(options[0],))

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
    @ui.page('/')
    def page():
        ui.select(
            [ui.as_option(val=v) for v in ('A', 'AB', 'XYZ')],
            with_input=True
        )

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
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.select([ui.as_option('A')], selected=(ui.as_option('A'),))

        def replace():
            container.clear()
            with container:
                ui.select([ui.as_option('B')], selected=(ui.as_option('B'),))
        ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('A')

    screen.click('Replace')
    screen.should_contain('B')
    screen.should_not_contain('A')


def test_multi_select(screen: Screen):
    options = [ui.as_option(v) for v in ('Alice', 'Bob', 'Carol')]

    @ui.page('/')
    def page():
        s = ui.select(options, selected=(options[0],), multiple=True).props('use-chips')
        ui.label().bind_text_from(s, 'value', lambda v: str(tuple(sorted(o.value for o in v))))

    screen.open('/')
    screen.should_contain("('Alice',)")
    screen.click('Alice')
    screen.click('Bob')
    screen.should_contain("('Alice', 'Bob')")

    screen.click('cancel')  # remove icon
    screen.should_contain("('Bob',)")


def test_changing_options(screen: Screen):
    options = [ui.as_option(v) for v in (10, 20, 30)]

    @ui.page('/')
    def page():
        s = ui.select(options, selected=(options[0],))
        ui.label().bind_text_from(s, 'value', backward=lambda v: f'value = {tuple(sorted(o.value for o in v))}')
        ui.button('reverse', on_click=lambda: (s.options.reverse(), s.update()))
        ui.button('clear', on_click=lambda: (s.options.clear(), s.update()))

    screen.open('/')
    screen.click('reverse')
    screen.should_contain('value = (10,)')
    screen.click('clear')
    screen.should_contain('value = ()')


def test_set_options(screen:  Screen):
    options = [ui.as_option(v) for v in (1, 2, 3)]
    new_options = [ui.as_option(v) for v in (4, 5, 6)]

    @ui.page('/')
    def page():
        s = ui.select(options, selected=(options[0],))
        ui.button('Set new options', on_click=lambda: s.set_options(new_options, value=(new_options[0],)))

    screen.open('/')
    screen.click('Set new options')
    screen.click('4')
    screen.should_contain('5')
    screen.should_contain('6')


@pytest.mark.parametrize('multiple', [False, True])
@pytest.mark.parametrize('new_value_mode', ['add', 'add-unique', 'toggle', None])
def test_add_new_values(screen:  Screen, multiple: bool, new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']]):
    options = [ui.as_option(v) for v in ('a', 'b', 'c')]

    @ui.page('/')
    def page():
        s = ui.select(
            options=options,
            multiple=multiple,
            new_value_mode=new_value_mode,
            new_val_to_option=lambda _, v: ui.as_option(v)
        )
        ui.label().bind_text_from(s, 'value', lambda v: f'value = {tuple(sorted(o.value for o in v))}')
        ui.label().bind_text_from(s, 'options', lambda v: f'options = {tuple(sorted(o.value for o in v))}')

    screen.open('/')

    screen.should_contain('value = ()')
    screen.should_contain("options = ('a', 'b', 'c')")

    screen.find_by_class('q-select').click()
    screen.wait(0.5)
    screen.find_all('a')[-1].click()
    screen.should_contain("value = ('a',)")

    if new_value_mode:
        for _ in range(2):
            screen.find_by_tag('input').send_keys(Keys.BACKSPACE + 'd')
            screen.wait(0.5)
            screen.find_by_tag('input').click()
            screen.wait(0.5)
            screen.find_by_tag('input').send_keys(Keys.ENTER)
            screen.wait(0.5)
        if new_value_mode == 'add':
            screen.should_contain("value = ('a', 'd', 'd')" if multiple else "value = ('d',)")
            screen.should_contain("options = ('a', 'b', 'c', 'd', 'd')")
        elif new_value_mode == 'add-unique':
            screen.should_contain("value = ('a', 'd')" if multiple else "value = ('d',)")
            screen.should_contain("options = ('a', 'b', 'c', 'd')")
        elif new_value_mode == 'toggle':
            screen.should_contain("value = ('a',)")
            screen.should_contain("options = ('a', 'b', 'c')")


def test_new_value_to_option(screen: Screen):
    options: list[ui.option[str, str]] = [
        ui.option(label='A', value='a'), ui.option(label='B', value='b'), ui.option(label='C', value='c')
    ]
    @ui.page('/')
    def page():
        select = ui.select(
            options,
            selected=(options[1],),
            new_value_mode='add',
            new_val_to_option=lambda s, v: ui.option(label=v.capitalize(), value=len(s.options))
        )
        ui.label().bind_text_from(select, 'options', lambda v: f'options = {dict((o.value, o.label) for o in v)}')

    screen.open('/')
    screen.find_by_tag('input').send_keys(Keys.BACKSPACE + 'd')
    screen.wait(0.5)
    screen.find_by_tag('input').send_keys(Keys.ENTER)
    screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C', 3: 'D'}")


@pytest.mark.parametrize('multiple', [False, True])
def test_keep_filtered_options(multiple: bool, screen: Screen):
    @ui.page('/')
    def page():
        ui.select(options=[ui.as_option(v) for v in ('A1', 'A2', 'B1', 'B2')], with_input=True, multiple=multiple)

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
    options = [ui.as_option(v) for v in ('A', 'BC', 'DEF')]

    @ui.page('/')
    def page():
        select = ui.select(options, selected=(options[0],), validation={'Too long': lambda v: len(v[0].value) < 3})
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
    @ui.page('/')
    def page():
        with pytest.raises(ValueError, match='Invalid values: X'):
            ui.select([ui.as_option(v) for v in ('A', 'B', 'C')], selected=(ui.as_option('X'),))

    screen.open('/')


@pytest.mark.parametrize('multiple', [False, True])
def test_opening_and_closing_popup_with_screen(multiple: bool, screen: Screen):
    select = None
    options = [ui.as_option(v) for v in ('Apple', 'Banana', 'Cherry')]

    @ui.page('/')
    def page():
        nonlocal select
        select = ui.select(options=options, label='Fruits', multiple=multiple).classes('w-24')
        ui.label().bind_text_from(select, 'is_showing_popup', lambda v: 'open' if v else 'closed')
        ui.label().bind_text_from(select, 'value', lambda v: f'value = {tuple(sorted(o.value for o in v))}')

    screen.open('/')
    fruits = screen.find_element(select)
    screen.should_contain('closed')

    fruits.click()
    screen.should_contain('open')
    fruits.click()
    screen.should_contain('closed')

    fruits.click()
    screen.click('Apple')
    if multiple:
        screen.click('Banana')
        screen.should_contain("value = ('Apple', 'Banana')")
        screen.should_contain('open')
    else:
        fruits.click()
        screen.click('Banana')
        screen.should_contain("value = ('Banana',)")
        screen.should_contain('closed')


@pytest.mark.parametrize('multiple', [False, True])
async def test_opening_and_closing_popup_with_user(multiple: bool, user: User):
    options = [ui.as_option(v) for v in ('Apple', 'Banana', 'Cherry')]

    @ui.page('/')
    def page():
        select = ui.select(options=options, label='Fruits', multiple=multiple)
        ui.label().bind_text_from(select, 'is_showing_popup', lambda v: 'open' if v else 'closed')
        ui.label().bind_text_from(select, 'value', lambda v: f'value = {v}')

    await user.open('/')
    fruits = user.find('Fruits')
    await user.should_see('closed')

    fruits.click()
    await user.should_see('open')
    fruits.click()
    await user.should_see('closed')

    fruits.click()
    user.find('Apple').click()
    if multiple:
        user.find('Banana').click()
        await user.should_see("value = ('Apple', 'Banana')")
        await user.should_see('open')
    else:
        fruits.click()
        user.find('Banana').click()
        await user.should_see("value = ('Banana',)")
        await user.should_see('closed')


def test_popup_scroll_behavior(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_css('html { scroll-behavior: smooth }')
        ui.link('Go to bottom', '#bottom')
        ui.link_target('bottom').classes('mt-[2000px]')
        ui.select(['apple', 'banana', 'cherry'], value='apple').props('behavior=dialog')

    screen.open('/')
    screen.click('Go to bottom')
    screen.wait(1)
    position = screen.selenium.execute_script('return window.scrollY')
    assert position > 1000

    screen.click('apple')
    screen.wait(0.5)
    screen.type(Keys.ESCAPE)
    screen.wait(0.2)
    assert screen.selenium.execute_script('return window.scrollY') == position
