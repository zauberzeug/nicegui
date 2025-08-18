import copy
import weakref
from typing import Dict, Optional, Tuple

from selenium.webdriver.common.keys import Keys

from nicegui import binding, ui
from nicegui.testing import Screen, User


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


async def test_copy_instance_with_bindable_property(user: User):
    @binding.bindable_dataclass
    class Number:
        value: int = 1

    x = Number()
    y = copy.copy(x)

    ui.label().bind_text_from(x, 'value', lambda v: f'x={v}')
    assert len(binding.bindings) == 1
    assert len(binding.active_links) == 0

    ui.label().bind_text_from(y, 'value', lambda v: f'y={v}')
    assert len(binding.bindings) == 2
    assert len(binding.active_links) == 0

    await user.open('/')
    await user.should_see('x=1')
    await user.should_see('y=1')

    y.value = 2
    await user.should_see('x=1')
    await user.should_see('y=2')


def test_automatic_cleanup(screen: Screen):
    class Model:
        value = binding.BindableProperty()

        def __init__(self, value: str) -> None:
            self.value = value

    def create_model_and_label(value: str) -> Tuple[int, weakref.ref, ui.label]:
        model = Model(value)
        label = ui.label(value).bind_text(model, 'value')
        return id(model), weakref.ref(model), label

    model_id1, ref1, label1 = create_model_and_label('first label')
    model_id2, ref2, _label2 = create_model_and_label('second label')

    def is_alive(ref: weakref.ref) -> bool:
        return ref() is not None

    def has_bindable_property(model_id: int) -> bool:
        return any(obj_id == model_id for obj_id, _ in binding.bindable_properties)

    screen.open('/')
    screen.should_contain('first label')
    screen.should_contain('second label')
    assert is_alive(ref1) and has_bindable_property(model_id1)
    assert is_alive(ref2) and has_bindable_property(model_id2)

    binding.remove([label1])
    assert not is_alive(ref1) and not has_bindable_property(model_id1)
    assert is_alive(ref2) and has_bindable_property(model_id2)


async def test_nested_propagation(user: User):
    class Demo:
        a = binding.BindableProperty()
        b = binding.BindableProperty(on_change=lambda obj, _: obj.change_a())

        def __init__(self) -> None:
            self.a = 0
            self.b = 0

        def change_a(self) -> None:
            self.a = 1
            self.a = 2

    demo = Demo()
    ui.label().bind_text_from(demo, 'a', lambda a: f'a = {a}')
    ui.number().bind_value_to(demo, 'b')  # should set a to 1 and then 2

    await user.open('/')
    await user.should_see('a = 2')  # the final value of a should be 2


def test_binding_check_other_exists_dict(screen: Screen):
    data: Dict[str, str] = {}
    label = ui.label()
    binding.bind(label, 'text', data, 'non_existent_key', check_other=True)

    screen.open('/')
    screen.assert_py_logger('WARNING',
                            'Binding a non-existing attribute "non_existent_key" of target object of type dict. '
                            'Proceeding with binding, keeping the value unset.')


def test_binding_check_exists_object(screen: Screen):
    class Model:
        attribute = 'existing-attribute'
    model = Model()
    label = ui.label()
    binding.bind(model, 'no_attribute', label, 'no_text')

    screen.open('/')
    screen.assert_py_logger('WARNING',
                            'Binding a non-existing attribute "no_attribute" of target object of type Model. '
                            'Proceeding with binding, keeping the value unset.')
    screen.assert_py_logger('WARNING',
                            'Binding a non-existing attribute "no_text" of target object of type Label. '
                            'Proceeding with binding, keeping the value unset.')


def test_binding_no_check_exists_with_dict(screen: Screen):
    data: Dict[str, str] = {}
    label = ui.label()
    binding.bind(data, 'non_existing_key', label, 'text')

    screen.open('/')
    # no warning
