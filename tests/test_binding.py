import copy
import weakref
from typing import Any

import pytest
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


@pytest.mark.parametrize('data_type', ['dict-dict', 'object-dict', 'dict-object'])
@pytest.mark.parametrize('initialize', [True, False])
async def test_nested_binding(data_type: str, initialize: bool, user: User):
    class Data:
        def __init__(self, config: dict[str, int]) -> None:
            self.config = config

    class Config:
        def __init__(self, volume: int) -> None:
            self.volume = volume

    data: Any
    if data_type == 'dict-dict':
        data = {'config': {'volume': 0}} if initialize else {}
    if data_type == 'object-dict':
        data = Data({'volume': 0} if initialize else {})
    if data_type == 'dict-object':
        data = {'config': Config(0)} if initialize else {}

    @ui.page('/')
    def page():
        ui.number('Volume', min=0, max=100, value=50).bind_value_to(data, ('config', 'volume'), forward=int)
        ui.label().bind_text_from(data, ('config', 'volume'), backward=lambda v: f'Volume: {v}%')
        with pytest.raises((KeyError, AttributeError), match=r'Could not bind non-existing'):
            ui.input().bind_value(data, ('x', 'y'), strict=True)
        with pytest.raises(AssertionError, match='cannot be empty'):
            ui.input().bind_value(data, ())
        with pytest.raises(AssertionError, match='cannot be empty'):
            ui.input().bind_value(data, '')
        with pytest.raises(AssertionError, match='must contain only strings'):
            ui.input().bind_value(data, ('valid', 123))  # type: ignore[arg-type]

    await user.open('/')
    await user.should_see('Volume: 50%')
    if data_type == 'dict-dict':
        assert data == {'config': {'volume': 50}}
    if data_type == 'object-dict':
        assert data.config == {'volume': 50}
    if data_type == 'dict-object':
        if initialize:
            assert data['config'].volume == 50
        else:
            assert data == {'config': {'volume': 50}}


# --- PROTOTYPE: reactive computed()/effect() on top of BindableProperty (see discussion #4758) ---

@binding.bindable_dataclass
class _Order:
    price: float = 10.0
    quantity: int = 2
    tax_rate: float = 0.0


def test_computed_derives_and_updates():
    binding.reset()
    order = _Order()
    subtotal = binding.computed(lambda: order.price * order.quantity)
    assert subtotal.value == 20
    order.price = 15
    assert subtotal.value == 30
    order.quantity = 4
    assert subtotal.value == 60
    assert binding.active_links == []  # no 0.1s refresh loop involved


def test_computed_chains_on_other_computed():
    binding.reset()
    order = _Order(tax_rate=0.1)
    subtotal = binding.computed(lambda: order.price * order.quantity)
    total = binding.computed(lambda: subtotal.value * (1 + order.tax_rate))
    assert total.value == 22
    order.price = 20
    assert subtotal.value == 40
    assert total.value == 44


def test_effect_runs_on_dependency_change_and_disposes():
    binding.reset()
    order = _Order()
    seen: list[float] = []
    handle = binding.effect(lambda: seen.append(order.price))
    assert seen == [10.0]
    order.price = 12
    assert seen == [10.0, 12.0]
    handle.dispose()
    order.price = 99
    assert seen == [10.0, 12.0]  # no longer reacting


@binding.bindable_dataclass
class _Toggle:
    on: bool = True
    a: int = 1
    b: int = 2


def test_effect_dependencies_are_dynamic():
    binding.reset()
    t = _Toggle()
    seen: list[int] = []
    handle = binding.effect(lambda: seen.append(t.a if t.on else t.b))  # retain: effects must be kept alive
    assert seen == [1]  # first run reads t.on and t.a (not t.b)
    t.b = 99  # t.b is not a dependency yet -> no re-run
    assert seen == [1]
    t.on = False  # re-run; now reads t.on and t.b -> switches dependency set
    assert seen == [1, 99]
    t.a = 5  # t.a is no longer a dependency -> no re-run
    assert seen == [1, 99]
    t.b = 7  # t.b is a dependency now -> re-run
    assert seen == [1, 99, 7]
    handle.dispose()
    t.b = 123  # disposed -> no re-run
    assert seen == [1, 99, 7]


@binding.bindable_dataclass
class _Num:
    n: int = 1


def test_diamond_effect_runs_once_glitch_free():
    """A single source change must update a diamond's sink exactly once, never on half-updated state.

    S -> A, S -> B, (A, B) -> effect. On one write to S, the effect must observe only fully-settled
    (A, B) and fire once for the change -- no intermediate (A=new, B=old) glitch, no double-run.
    """
    binding.reset()
    src = _Num(n=1)
    a = binding.computed(lambda: src.n + 1)   # 2
    b = binding.computed(lambda: src.n + 10)  # 11
    seen: list[tuple[int, int]] = []
    handle = binding.effect(lambda: seen.append((a.value, b.value)))
    assert seen == [(2, 11)]
    src.n = 2
    assert seen == [(2, 11), (3, 12)]  # ONE consistent update; not [..., (3, 11), (3, 12)]
    handle.dispose()


def test_diamond_computed_on_computed_runs_once():
    """A computed sink over a diamond recomputes once with consistent inputs on a single source write."""
    binding.reset()
    src = _Num(n=1)
    a = binding.computed(lambda: src.n + 1)   # 2
    b = binding.computed(lambda: src.n + 10)  # 11
    runs: list[float] = []

    def total_fn() -> float:
        runs.append(1)
        return a.value + b.value

    total = binding.computed(total_fn)
    assert total.value == 13  # 2 + 11
    runs_before = len(runs)
    src.n = 2
    assert total.value == 15  # 3 + 12
    assert len(runs) == runs_before + 1  # recomputed exactly once for the change, not twice


def test_batch_coalesces_writes():
    """Multiple writes inside binding.batch() collapse into one flush -> one effect re-run."""
    binding.reset()
    order = _Order()  # price=10.0, quantity=2
    runs: list[float] = []
    handle = binding.effect(lambda: runs.append(order.price + order.quantity))
    assert runs == [12.0]
    with binding.batch():
        order.price = 5
        order.quantity = 9
    assert runs == [12.0, 14.0]  # coalesced: initial + ONE, not initial + two
    handle.dispose()


def test_no_batch_reruns_per_write():
    """Without batch(), each write flushes synchronously (read-after-write stays synchronous)."""
    binding.reset()
    order = _Order()
    runs: list[float] = []
    handle = binding.effect(lambda: runs.append(order.price + order.quantity))
    assert runs == [12.0]
    order.price = 5      # -> 7.0
    order.quantity = 9   # -> 14.0
    assert runs == [12.0, 7.0, 14.0]
    handle.dispose()


def test_equality_cutoff_stops_propagation():
    """An unchanged write (or a computed that recomputes to the same value) must not re-run dependents."""
    binding.reset()
    order = _Order()
    runs: list[float] = []
    doubled = binding.computed(lambda: order.price * 2)
    handle = binding.effect(lambda: runs.append(doubled.value))
    assert runs == [20.0]
    order.price = 10  # 10 == 10.0 -> no change -> no re-run
    assert runs == [20.0]
    handle.dispose()


def test_effect_writing_its_own_dependency_converges():
    """An effect that writes a signal it reads must run to convergence, not stop after one run.

    Regression guard: the earlier "skip currently-running subscribers" heuristic silently dropped
    this re-invalidation. The fix only skips a subscriber that is pulling the just-changed producer
    as a fresh read (the diamond case), so a genuine post-read write still schedules a re-run.
    """
    binding.reset()
    state = _Num(n=0)
    seen: list[int] = []

    def fn() -> None:
        seen.append(state.n)
        if state.n < 3:
            state.n = state.n + 1

    handle = binding.effect(fn)
    assert seen == [0, 1, 2, 3]  # converged, not [0]
    assert state.n == 3
    handle.dispose()


def test_disposed_subscriptions_are_pruned():
    """Re-running/disposing computations must not leave empty subscriber entries behind (churn leak)."""
    binding.reset()
    state = _Num(n=0)
    handles = [binding.effect(lambda: state.n) for _ in range(50)]
    assert len(binding._subscribers) >= 1
    for handle in handles:
        handle.dispose()
    assert len(binding._subscribers) == 0  # every emptied entry pruned


@binding.bindable_dataclass
class _DiamondState:
    s: int = 1


async def test_computed_drives_bound_ui_label(user: User):
    """A real ui.label bound to computed() updates on a source change -- zero new element API.

    Exercises the diamond end-to-end: the label binds to C = A + B, both derived from S.
    """
    state = _DiamondState(s=1)
    a = binding.computed(lambda: state.s + 1)
    b = binding.computed(lambda: state.s + 10)
    total = binding.computed(lambda: a.value + b.value)  # C = A + B = 13 at s=1

    @ui.page('/')
    def page():
        ui.label().bind_text_from(total, 'value', backward=lambda v: f'total={v}')

    await user.open('/')
    await user.should_see('total=13')
    state.s = 2  # A=3, B=12 -> C=15
    await user.should_see('total=15')


@binding.bindable_dataclass
class _Branch:
    flag: bool = False
    a: int = 0
    b: int = 0


def test_dispose_unsubscribes_even_when_effect_raised():
    """Deps read before an exception must still be unsubscribed by dispose() (no zombie re-runs)."""
    binding.reset()
    br = _Branch()
    runs: list[bool] = []

    def fn() -> None:
        runs.append(br.flag)
        if br.flag:
            _ = br.a  # newly-read dependency...
            raise ValueError('boom')  # ...then raise before the run completes
        _ = br.b

    handle = binding.effect(fn)
    with pytest.raises(ValueError, match='boom'):
        br.flag = True  # triggers the raising run
    handle.dispose()
    runs.clear()
    br.a = 1  # must NOT resurrect the disposed effect
    assert runs == []


def test_cycle_error_does_not_poison_later_writes():
    """After a cycle RuntimeError, the scheduler must recover for unrelated reactive work."""
    binding.reset()
    loop = _Num(n=0)
    with pytest.raises(RuntimeError, match='cycle'):
        binding.effect(lambda: setattr(loop, 'n', loop.n + 1))  # unbounded feedback
    assert binding._pending == set()  # poisoned state cleared

    other = _Num(n=0)
    seen: list[int] = []
    handle = binding.effect(lambda: seen.append(other.n))  # retain: effects are held weakly
    other.n = 5  # unrelated write must work normally, not re-raise the old cycle
    assert seen == [0, 5]
    handle.dispose()
