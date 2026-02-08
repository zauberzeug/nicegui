import copy
import weakref

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nicegui import binding, ui
from nicegui.testing import Screen, User


def test_ui_select_with_tuple_as_key(screen: Screen):
    class Model:
        selection: tuple[int, int] | None = None
    data = Model()
    options = {
        (2, 1): 'option A',
        (1, 2): 'option B',
    }
    data.selection = next(iter(options))

    @ui.page('/')
    def page():
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

    @ui.page('/')
    def page():
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

    @ui.page('/')
    def page():
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
    element = None

    @ui.page('/')
    def page():
        nonlocal element
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
    data: dict = {}

    @ui.page('/')
    def page():
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

    @ui.page('/')
    def page():
        ui.label().bind_text_from(instance, 'not_bindable')
        ui.label().bind_text_from(instance, 'bindable')

    screen.open('/')
    screen.should_contain('not_bindable_text')
    screen.should_contain('bindable_text')

    assert len(binding.bindings) == 2
    assert len(binding.active_links) == 1
    assert binding.active_links[0][1] == ('not_bindable',)  # Names are now normalized to tuples


async def test_copy_instance_with_bindable_property(user: User):
    @binding.bindable_dataclass
    class Number:
        value: int = 1

    x = Number()
    y = copy.copy(x)

    @ui.page('/')
    def page():
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

    def create_model_and_label(value: str) -> tuple[int, weakref.ref, ui.label]:
        model = Model(value)
        label = ui.label(value).bind_text(model, 'value')
        return id(model), weakref.ref(model), label

    model_id1 = ref1 = label1 = model_id2 = ref2 = label2 = None

    @ui.page('/')
    def page():
        nonlocal model_id1, ref1, label1, model_id2, ref2, label2
        model_id1, ref1, label1 = create_model_and_label('first label')
        model_id2, ref2, label2 = create_model_and_label('second label')

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

    @ui.page('/')
    def page():
        ui.label().bind_text_from(demo, 'a', lambda a: f'a = {a}')
        ui.number().bind_value_to(demo, 'b')  # should set a to 1 and then 2

    await user.open('/')
    await user.should_see('a = 2')  # the final value of a should be 2


def test_binding_other_dict_is_strict(screen: Screen):
    data: dict[str, str] = {}

    @ui.page('/')
    def page():
        label = ui.label()
        with pytest.raises(KeyError):
            binding.bind(label, 'text', data, 'non_existent_key', other_strict=True)

    screen.open('/')


def test_binding_object_is_strict(screen: Screen):
    class Model:
        attribute = 'existing-attribute'
    model = Model()

    @ui.page('/')
    def page():
        label = ui.label()
        with pytest.raises(AttributeError):
            binding.bind(model, 'no_attribute', label, 'no_text')

    screen.open('/')


def test_binding_dict_is_not_strict(screen: Screen):
    data: dict[str, str] = {}

    @ui.page('/')
    def page():
        label = ui.label()
        binding.bind(data, 'non_existing_key', label, 'text')  # no exception

    screen.open('/')


def test_binding_refresh_interval_none(screen: Screen):
    class Model:
        value = 0

    @ui.page('/')
    def page():
        ui.label().bind_text_from(Model, 'value', lambda value: f'Value is {value}')

    screen.ui_run_kwargs['binding_refresh_interval'] = None
    screen.open('/')
    screen.should_contain('Value is 0')
    screen.assert_py_logger(
        'WARNING', 'Starting active binding loop even though it was disabled via binding_refresh_interval=None.',
    )

def test_nested_dict_binding(screen: Screen):
    """Test basic nested dictionary binding with tuple syntax."""
    data = {}

    @ui.page('/')
    def page():
        ui.input('Username').bind_value(data, ('profile', 'username'))

    screen.open('/')
    screen.type(Keys.TAB)  # Focus the input
    screen.type('Alice')
    screen.type(Keys.TAB)  # Commit the value
    screen.wait(0.1)

    assert 'profile' in data
    assert data['profile']['username'] == 'Alice'


def test_nested_auto_creation(screen: Screen):
    """Test that intermediate dictionaries are auto-created."""
    data: dict = {}

    @ui.page('/')
    def page():
        ui.input().bind_value(data, ('a', 'b', 'c'))

    screen.open('/')
    screen.type(Keys.TAB)
    screen.type('value')
    screen.type(Keys.TAB)
    screen.wait(0.1)

    # Check that nested structure was created
    assert 'a' in data
    assert 'b' in data['a']
    assert 'c' in data['a']['b']
    assert data['a']['b']['c'] == 'value'


def test_nested_storage_binding(screen: Screen):
    """Test binding to nested keys in storage."""
    # Use a simple dict instead of app.storage to avoid storage_secret requirement
    storage = {}

    @ui.page('/')
    def page():
        ui.input().bind_value(storage, ('settings', 'theme'))
        ui.label().bind_text_from(storage, ('settings', 'theme'))

    screen.open('/')
    screen.type(Keys.TAB)
    screen.type('dark')
    screen.type(Keys.TAB)
    screen.wait(0.1)

    assert 'settings' in storage
    assert storage['settings']['theme'] == 'dark'
    screen.should_contain('dark')


def test_nested_with_transformation(screen: Screen):
    """Test nested binding with forward/backward transformations."""
    data = {}

    @ui.page('/')
    def page():
        ui.number('Volume', min=0, max=100, value=50).bind_value_to(
            data, ('config', 'volume'),
            forward=int
        )
        ui.label().bind_text_from(
            data, ('config', 'volume'),
            backward=lambda v: f'Volume: {v}%'
        )

    screen.open('/')
    screen.wait(0.1)
    screen.should_contain('Volume: 50%')


def test_single_key_backward_compatible(screen: Screen):
    """Ensure single string keys still work exactly as before."""
    data = {}

    @ui.page('/')
    def page():
        ui.input().bind_value(data, 'name')  # Old style

    screen.open('/')
    screen.type(Keys.TAB)  # Focus the input
    screen.type('Alice')
    screen.type(Keys.TAB)  # Commit
    screen.wait(0.1)

    assert data['name'] == 'Alice'


def test_mixed_object_dict_nesting(screen: Screen):
    """Test binding through mixed object attributes and dict keys."""
    class Config:
        def __init__(self):
            self.data = {}

    config = Config()

    @ui.page('/')
    def page():
        ui.input().bind_value(config, ('data', 'username'))

    screen.open('/')
    screen.type(Keys.TAB)
    screen.type('test')
    screen.type(Keys.TAB)
    screen.wait(0.1)

    assert 'username' in config.data
    assert config.data['username'] == 'test'


def test_nested_strict_mode_validation(screen: Screen):
    """Test that strict mode validates nested paths correctly."""
    data = {}

    @ui.page('/')
    def page():
        with pytest.raises(KeyError, match=r'non-existing key "a->b->c"'):
            ui.input().bind_value(data, ('a', 'b', 'c'), strict=True)

    screen.open('/')


def test_single_key_strict_mode_validation(screen: Screen):
    """Test that strict mode validates single keys correctly."""
    data = {}

    @ui.page('/')
    def page():
        with pytest.raises(KeyError, match=r'non-existing key "missing"'):
            ui.input().bind_value(data, 'missing', strict=True)

    screen.open('/')


def test_deep_nesting(screen: Screen):
    """Test binding with 4+ nested levels."""
    data = {}

    @ui.page('/')
    def page():
        ui.input().bind_value(data, ('level1', 'level2', 'level3', 'level4'))

    screen.open('/')
    screen.type(Keys.TAB)
    screen.type('deep')
    screen.type(Keys.TAB)
    screen.wait(0.1)

    # Check nested structure was created
    assert 'level1' in data
    assert 'level2' in data['level1']
    assert 'level3' in data['level1']['level2']
    assert 'level4' in data['level1']['level2']['level3']
    assert data['level1']['level2']['level3']['level4'] == 'deep'


def test_nested_visibility_binding(screen: Screen):
    """Test nested binding works with visibility."""
    data = {'ui': {'sidebar': {'visible': True}}}

    @ui.page('/')
    def page():
        with ui.column().bind_visibility_from(data, ('ui', 'sidebar', 'visible')).classes('test-column'):
            ui.label('Content')

    screen.open('/')
    screen.should_contain('Content')
    # Verify the column is initially visible (no 'hidden' class)
    columns = screen.selenium.find_elements(By.CSS_SELECTOR, '.test-column.hidden')
    assert len(columns) == 0, 'Column should be visible when visibility is True'

    # Change visibility to False and verify
    data['ui']['sidebar']['visible'] = False
    screen.wait(0.5)
    # Content should still exist in DOM but be hidden
    screen.should_not_contain('Content')
    # Verify the 'hidden' class is applied when visibility is False
    columns = screen.selenium.find_elements(By.CSS_SELECTOR, '.test-column.hidden')
    assert len(columns) > 0, 'Column should be hidden when visibility is False'


def test_generic_bind_with_tuple(screen: Screen):
    """Test that generic bind() function accepts tuple syntax."""
    data1 = {'config': {'message': 'Hello'}}

    @ui.page('/')
    def page():
        label = ui.label()
        binding.bind(label, 'text', data1, ('config', 'message'))

    screen.open('/')
    screen.wait(0.1)
    screen.should_contain('Hello')


def test_nested_text_binding(screen: Screen):
    """Test nested binding with text elements."""
    data = {}

    @ui.page('/')
    def page():
        ui.label().bind_text_from(data, ('messages', 'welcome'))

    data['messages'] = {'welcome': 'Welcome!'}
    screen.open('/')
    screen.wait(0.1)
    screen.should_contain('Welcome!')


def test_nested_enabled_binding(screen: Screen):
    """Test nested binding with enabled/disabled elements."""
    data = {'ui': {'button': {'enabled': False}}}

    @ui.page('/')
    def page():
        ui.button('Click').bind_enabled_from(data, ('ui', 'button', 'enabled')).classes('test-button')

    screen.open('/')
    screen.wait(0.1)
    # Verify the button is disabled initially
    button = screen.selenium.find_element(By.CSS_SELECTOR, '.test-button')
    assert button.get_attribute('aria-disabled') == 'true' or button.get_attribute('disabled') is not None, \
        'Button should be disabled when enabled is False'

    # Change to enabled and verify
    data['ui']['button']['enabled'] = True
    screen.wait(0.5)
    button = screen.selenium.find_element(By.CSS_SELECTOR, '.test-button')
    assert button.get_attribute('aria-disabled') != 'true' and button.get_attribute('disabled') is None, \
        'Button should be enabled when enabled is True'


def test_default_parameter_still_works(screen: Screen):
    """Test that calling bind methods without additional args still works."""
    class Model:
        value = 'test'

    data = Model()

    @ui.page('/')
    def page():
        # Should default to 'value' property
        ui.input().bind_value_from(data)

    screen.open('/')
    screen.should_contain_input('test')


def test_empty_tuple_validation(screen: Screen):
    """Test that empty tuples are rejected with clear error messages."""
    data = {}

    @ui.page('/')
    def page():
        with pytest.raises(ValueError, match='cannot be empty'):
            ui.input().bind_value(data, ())

    screen.open('/')


def test_empty_string_validation(screen: Screen):
    """Test that empty strings are rejected with clear error messages."""
    data = {}

    @ui.page('/')
    def page():
        with pytest.raises(ValueError, match='cannot be an empty string'):
            ui.input().bind_value(data, '')

    screen.open('/')


def test_non_string_tuple_validation(screen: Screen):
    """Test that tuples with non-string elements are rejected."""
    data = {}

    @ui.page('/')
    def page():
        with pytest.raises(ValueError, match='must contain only strings'):
            ui.input().bind_value(data, ('valid', 123))  # type: ignore[arg-type]

    screen.open('/')
