from typing import Dict, Optional, Tuple

from selenium.webdriver.common.keys import Keys

from nicegui import binding, ui
from nicegui.testing import Screen


def test_ui_select_with_tuple_as_key(screen: Screen):
    class Model:
        selection: Optional[Tuple[int, int]] = None
    data = Model()
    options = {
        (2, 1): 'option A',
        (1, 2): 'option B',
    }
    data.selection = next(iter(options))
    ui.select(options).bind_value(data, 'selection')

    screen.open('/')
    screen.should_not_contain('option B')
    element = screen.click('option A')
    screen.click_at_position(element, x=20, y=100)
    screen.wait(0.3)
    screen.should_contain('option B')
    screen.should_not_contain('option A')
    assert data.selection == (1, 2)


def test_ui_select_with_list_of_tuples(screen: Screen):
    class Model:
        selection = None
    data = Model()
    options = [(1, 1), (2, 2), (3, 3)]
    data.selection = options[0]
    ui.select(options).bind_value(data, 'selection')

    screen.open('/')
    screen.should_not_contain('2,2')
    element = screen.click('1,1')
    screen.click_at_position(element, x=20, y=100)
    screen.wait(0.3)
    screen.should_contain('2,2')
    screen.should_not_contain('1,1')
    assert data.selection == (2, 2)


def test_ui_select_with_list_of_lists(screen: Screen):
    class Model:
        selection = None
    data = Model()
    options = [[1, 1], [2, 2], [3, 3]]
    data.selection = options[0]
    ui.select(options).bind_value(data, 'selection')

    screen.open('/')
    screen.should_not_contain('2,2')
    element = screen.click('1,1')
    screen.click_at_position(element, x=20, y=100)
    screen.wait(0.3)
    screen.should_contain('2,2')
    screen.should_not_contain('1,1')
    assert data.selection == [2, 2]


def test_binding_to_input(screen: Screen):
    class Model:
        text = 'one'
    data = Model()
    element = ui.input().bind_value(data, 'text')

    screen.open('/')
    screen.should_contain_input('one')
    screen.type(Keys.TAB)
    screen.type('two')
    screen.should_contain_input('two')
    screen.wait(0.1)
    assert data.text == 'two'
    data.text = 'three'
    screen.should_contain_input('three')
    element.set_value('four')
    screen.should_contain_input('four')
    assert data.text == 'four'
    element.value = 'five'
    screen.should_contain_input('five')
    assert data.text == 'five'


def test_binding_refresh_before_page_delivery(screen: Screen):
    state = {'count': 0}

    @ui.page('/')
    def main_page() -> None:
        ui.label().bind_text_from(state, 'count')
        state['count'] += 1

    screen.open('/')
    screen.should_contain('1')


def test_missing_target_attribute(screen: Screen):
    data: Dict = {}
    ui.label('Hello').bind_text_to(data)
    ui.label().bind_text_from(data, 'text', lambda text: f'{text=}')

    screen.open('/')
    screen.should_contain("text='Hello'")


def test_bindable_dataclass(screen: Screen):
    @binding.bindable_dataclass(bindable_fields=['bindable'])
    class TestClass:
        not_bindable: str = 'not_bindable_text'
        bindable: str = 'bindable_text'

    instance = TestClass()

    ui.label().bind_text_from(instance, 'not_bindable')
    ui.label().bind_text_from(instance, 'bindable')

    screen.open('/')
    screen.should_contain('not_bindable_text')
    screen.should_contain('bindable_text')

    assert len(binding.bindings) == 2
    assert len(binding.active_links) == 1
    assert binding.active_links[0][1] == 'not_bindable'
