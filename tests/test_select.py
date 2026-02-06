import pytest
from selenium.webdriver import Keys

from nicegui import ui
from nicegui.testing import SharedScreen, User


def test_select(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.select(['A', 'B', 'C'], value='A')

    shared_screen.open('/')
    shared_screen.should_contain('A')
    shared_screen.should_not_contain('B')
    shared_screen.should_not_contain('C')

    shared_screen.click('A')  # open the dropdown
    shared_screen.click('B')  # close the dropdown
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('A')
    shared_screen.should_contain('B')
    shared_screen.should_not_contain('C')


def test_select_with_input(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.select(['A', 'AB', 'XYZ'], with_input=True)

    shared_screen.open('/')
    shared_screen.find_by_tag('input').click()
    shared_screen.should_contain('XYZ')

    shared_screen.find_by_tag('input').send_keys('A')
    shared_screen.wait(0.5)
    shared_screen.should_contain('A')
    shared_screen.should_contain('AB')
    shared_screen.should_not_contain('XYZ')

    shared_screen.find_by_tag('input').send_keys('ABC' + Keys.ENTER)
    shared_screen.find_by_tag('input').click()
    shared_screen.should_not_contain('ABC')


def test_replace_select(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.select(['A'], value='A')

        def replace():
            with container.clear():
                ui.select(['B'], value='B')
        ui.button('Replace', on_click=replace)

    shared_screen.open('/')
    shared_screen.should_contain('A')

    shared_screen.click('Replace')
    shared_screen.should_contain('B')
    shared_screen.should_not_contain('A')


def test_multi_select(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        s = ui.select(['Alice', 'Bob', 'Carol'], value='Alice', multiple=True).props('use-chips')
        ui.label().bind_text_from(s, 'value', backward=str)

    shared_screen.open('/')
    shared_screen.should_contain("['Alice']")
    shared_screen.click('Alice')
    shared_screen.click('Bob')
    shared_screen.should_contain("['Alice', 'Bob']")

    shared_screen.click('cancel')  # remove icon
    shared_screen.should_contain("['Bob']")


def test_changing_options(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        s = ui.select([10, 20, 30], value=10)
        ui.label().bind_text_from(s, 'value', lambda v: f'value = {v}')
        ui.button('reverse', on_click=lambda: (s.options.reverse(), s.update()))
        ui.button('clear', on_click=lambda: (s.options.clear(), s.update()))

    shared_screen.open('/')
    shared_screen.click('reverse')
    shared_screen.should_contain('value = 10')
    shared_screen.click('clear')
    shared_screen.should_contain('value = None')


def test_set_options(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        s = ui.select([1, 2, 3], value=1)
        ui.button('Set new options', on_click=lambda: s.set_options([4, 5, 6], value=4))

    shared_screen.open('/')
    shared_screen.click('Set new options')
    shared_screen.click('4')
    shared_screen.should_contain('5')
    shared_screen.should_contain('6')


@pytest.mark.parametrize('option_dict', [False, True])
@pytest.mark.parametrize('multiple', [False, True])
@pytest.mark.parametrize('new_value_mode', ['add', 'add-unique', 'toggle', None])
def test_add_new_values(shared_screen: SharedScreen, option_dict: bool, multiple: bool, new_value_mode: str | None):
    @ui.page('/')
    def page():
        options = {'a': 'A', 'b': 'B', 'c': 'C'} if option_dict else ['a', 'b', 'c']
        s = ui.select(options=options, multiple=multiple, new_value_mode=new_value_mode)
        ui.label().bind_text_from(s, 'value', lambda v: f'value = {v}')
        ui.label().bind_text_from(s, 'options', lambda v: f'options = {v}')

    shared_screen.open('/')
    if option_dict and new_value_mode == 'add':
        shared_screen.allowed_js_errors.append('500 (Internal Server Error)')
        shared_screen.assert_py_logger('ERROR', 'new_value_mode "add" is not supported for dict options without key_generator')
        return

    shared_screen.should_contain('value = []' if multiple else 'value = None')
    shared_screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C'}" if option_dict else "options = ['a', 'b', 'c']")

    shared_screen.find_by_class('q-select').click()
    shared_screen.wait(0.5)
    shared_screen.find_all('A' if option_dict else 'a')[-1].click()
    shared_screen.should_contain("value = ['a']" if multiple else 'value = a')

    if new_value_mode:
        for _ in range(2):
            shared_screen.find_by_tag('input').send_keys(Keys.BACKSPACE + 'd')
            shared_screen.wait(0.5)
            shared_screen.find_by_tag('input').click()
            shared_screen.wait(0.5)
            shared_screen.find_by_tag('input').send_keys(Keys.ENTER)
            shared_screen.wait(0.5)
        if new_value_mode == 'add':
            shared_screen.should_contain("value = ['a', 'd', 'd']" if multiple else 'value = d')
            shared_screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'd', 'd': 'd'}" if option_dict else
                                  "options = ['a', 'b', 'c', 'd', 'd']")
        elif new_value_mode == 'add-unique':
            shared_screen.should_contain("value = ['a', 'd']" if multiple else 'value = d')
            shared_screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'd'}" if option_dict else
                                  "options = ['a', 'b', 'c', 'd']")
        elif new_value_mode == 'toggle':
            shared_screen.should_contain("value = ['a']" if multiple else 'value = None')
            shared_screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C'}" if option_dict else
                                  "options = ['a', 'b', 'c']")


def test_id_generator(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        options = {'a': 'A', 'b': 'B', 'c': 'C'}
        select = ui.select(options, value='b', new_value_mode='add', key_generator=lambda _: len(options))
        ui.label().bind_text_from(select, 'options', lambda v: f'options = {v}')

    shared_screen.open('/')
    shared_screen.find_by_tag('input').send_keys(Keys.BACKSPACE + 'd')
    shared_screen.wait(0.5)
    shared_screen.find_by_tag('input').send_keys(Keys.ENTER)
    shared_screen.should_contain("options = {'a': 'A', 'b': 'B', 'c': 'C', 3: 'd'}")


@pytest.mark.parametrize('multiple', [False, True])
def test_keep_filtered_options(multiple: bool, shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.select(options=['A1', 'A2', 'B1', 'B2'], with_input=True, multiple=multiple)

    shared_screen.open('/')
    shared_screen.find_by_tag('input').click()
    shared_screen.should_contain('A1')
    shared_screen.should_contain('A2')
    shared_screen.should_contain('B1')
    shared_screen.should_contain('B2')

    shared_screen.find_by_tag('input').send_keys('A')
    shared_screen.wait(0.5)
    shared_screen.should_contain('A1')
    shared_screen.should_contain('A2')
    shared_screen.should_not_contain('B1')
    shared_screen.should_not_contain('B2')

    shared_screen.click('A1')
    shared_screen.wait(0.5)
    shared_screen.find_by_tag('input').click()
    shared_screen.should_contain('A1')
    shared_screen.should_contain('A2')
    if multiple:
        shared_screen.should_not_contain('B1')
        shared_screen.should_not_contain('B2')
    else:
        shared_screen.should_contain('B1')
        shared_screen.should_contain('B2')


@pytest.mark.parametrize('auto_validation', [True, False])
def test_select_validation(auto_validation: bool, shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        select = ui.select(['A', 'BC', 'DEF'], value='A', validation={'Too long': lambda v: len(v) < 3})
        if not auto_validation:
            select.without_auto_validation()

    shared_screen.open('/')
    shared_screen.click('A')
    shared_screen.click('DEF')
    shared_screen.wait(0.5)
    if auto_validation:
        shared_screen.should_contain('Too long')
    else:
        shared_screen.should_not_contain('Too long')


def test_invalid_value(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with pytest.raises(ValueError, match='Invalid value: X'):
            ui.select(['A', 'B', 'C'], value='X')

    shared_screen.open('/')


@pytest.mark.parametrize('multiple', [False, True])
def test_opening_and_closing_popup_with_screen(multiple: bool, shared_screen: SharedScreen):
    select = None

    @ui.page('/')
    def page():
        nonlocal select
        select = ui.select(options=['Apple', 'Banana', 'Cherry'], label='Fruits', multiple=multiple).classes('w-24')
        ui.label().bind_text_from(select, 'is_showing_popup', lambda v: 'open' if v else 'closed')
        ui.label().bind_text_from(select, 'value', lambda v: f'value = {v}')

    shared_screen.open('/')
    fruits = shared_screen.find_element(select)
    shared_screen.should_contain('closed')

    fruits.click()
    shared_screen.should_contain('open')
    fruits.click()
    shared_screen.should_contain('closed')

    fruits.click()
    shared_screen.click('Apple')
    if multiple:
        shared_screen.click('Banana')
        shared_screen.should_contain("value = ['Apple', 'Banana']")
        shared_screen.should_contain('open')
    else:
        fruits.click()
        shared_screen.click('Banana')
        shared_screen.should_contain('value = Banana')
        shared_screen.should_contain('closed')


@pytest.mark.parametrize('multiple', [False, True])
async def test_opening_and_closing_popup_with_user(multiple: bool, user: User):
    @ui.page('/')
    def page():
        select = ui.select(options=['Apple', 'Banana', 'Cherry'], label='Fruits', multiple=multiple)
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
        await user.should_see("value = ['Apple', 'Banana']")
        await user.should_see('open')
    else:
        fruits.click()
        user.find('Banana').click()
        await user.should_see('value = Banana')
        await user.should_see('closed')


def test_popup_scroll_behavior(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.add_css('html { scroll-behavior: smooth }')
        ui.link('Go to bottom', '#bottom')
        ui.link_target('bottom').classes('mt-[2000px]')
        ui.select(['apple', 'banana', 'cherry'], value='apple').props('behavior=dialog')

    shared_screen.open('/')
    shared_screen.click('Go to bottom')
    shared_screen.wait(1)
    position = shared_screen.selenium.execute_script('return window.scrollY')
    assert position > 1000

    shared_screen.click('apple')
    shared_screen.wait(0.5)
    shared_screen.type(Keys.ESCAPE)
    shared_screen.wait(0.2)
    assert shared_screen.selenium.execute_script('return window.scrollY') == position
