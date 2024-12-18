import gc
import weakref
from typing import Dict, Optional, Tuple

from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.binding import bindable_properties, BindableProperty, remove
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


class TestBindablePropertyAutomaticCleanup:
    @staticmethod
    def make_label_bound_to_model(value: str) -> Tuple[ui.label, int, weakref.ref]:
        class Model:
            value = BindableProperty()

            def __init__(self, value: str) -> None:
                self.value = value

        model = Model(value)
        label = ui.label(model.value).bind_text(model, 'value')

        return label, id(model), weakref.ref(model)

    @staticmethod
    def remove_bindings(*elements: ui.element) -> None:
        remove(elements)  # usually the client calls this function on its elements when the user disconnects
        gc.collect()  # should not really be necessary, but better safe than sorry

    def test_model_automatic_cleanup(self, screen: Screen):
        label, model_id, model_ref = self.make_label_bound_to_model('some value')

        screen.open('/')
        screen.should_contain('some value')

        def model_is_alive() -> bool:
            return model_ref() is not None

        def model_has_bindings() -> bool:
            return any(obj_id == model_id for obj_id, _ in bindable_properties)

        assert model_is_alive()
        assert model_has_bindings()

        self.remove_bindings(label)

        assert not model_is_alive()
        assert not model_has_bindings()

    def test_only_dead_model_unregistered(self, screen: Screen):
        label_1, first_id, first_ref = self.make_label_bound_to_model('first')
        _, second_id, second_ref = self.make_label_bound_to_model('second')

        screen.open('/')
        screen.should_contain('first')
        screen.should_contain('second')

        def is_alive(ref: weakref.ref) -> bool:
            return ref() is not None

        def has_bindings(owner: int) -> bool:
            return any(obj_id == owner for obj_id, _ in bindable_properties)

        assert is_alive(first_ref)
        assert has_bindings(first_id)

        assert is_alive(second_ref)
        assert has_bindings(second_id)

        self.remove_bindings(label_1)

        assert not is_alive(first_ref)
        assert not has_bindings(first_id)

        assert is_alive(second_ref)
        assert has_bindings(second_id)
