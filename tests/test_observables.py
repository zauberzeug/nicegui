import asyncio
import copy

import pytest

from nicegui import helpers, ui
from nicegui.events import ObservableChangeEventArguments
from nicegui.observables import ObservableDict, ObservableList, ObservableSet
from nicegui.testing import Screen, User

# pylint: disable=global-statement
count = 0


def reset_counter():
    global count  # noqa: PLW0603
    count = 0


def increment_counter():
    global count  # noqa: PLW0603
    count += 1


async def increment_counter_slowly(_):
    global count  # noqa: PLW0603
    await asyncio.sleep(0.1)
    count += 1


def test_observable_dict():
    reset_counter()
    data = ObservableDict(on_change=increment_counter)
    data['a'] = 1
    assert count == 1
    del data['a']
    assert count == 2
    data.update({'b': 2, 'c': 3})
    assert count == 3
    data.pop('b')
    assert count == 4
    data.popitem()
    assert count == 5
    data.clear()
    assert count == 6
    data.setdefault('a', 1)
    assert count == 7
    data |= {'b': 2}
    assert count == 8


def test_observable_list():
    reset_counter()
    data = ObservableList(on_change=increment_counter)
    data.append(1)
    assert count == 1
    data.extend([2, 3, 4])
    assert count == 2
    data.insert(0, 0)
    assert count == 3
    data.remove(1)
    assert count == 4
    data.pop(-1)
    assert count == 5
    data.sort()
    assert count == 6
    data.reverse()
    assert count == 7
    data[0] = 1
    assert count == 8
    data[0:2] = [1, 2, 3]
    assert count == 9
    del data[0]
    assert count == 10
    del data[0:1]
    assert count == 11
    data.clear()
    assert count == 12
    data += [1, 2, 3]
    assert count == 13


def test_observable_set():
    reset_counter()
    data = ObservableSet({1, 2, 3, 4, 5}, on_change=increment_counter)
    data.add(1)
    assert count == 1
    data.remove(1)
    assert count == 2
    data.discard(2)
    assert count == 3
    data.pop()
    assert count == 4
    data.clear()
    assert count == 5
    data.update({1, 2, 3})
    assert count == 6
    data.intersection_update({1, 2})
    assert count == 7
    data.difference_update({1})
    assert count == 8
    data.symmetric_difference_update({1, 2})
    assert count == 9
    data |= {1, 2, 3}
    assert count == 10
    data &= {1, 2}
    assert count == 11
    data -= {1}
    assert count == 12
    data ^= {1, 2}
    assert count == 13


def test_nested_observables():
    reset_counter()
    data = ObservableDict({
        'a': 1,
        'b': [1, 2, 3, {'x': 1, 'y': 2, 'z': 3}],
        'c': {'x': 1, 'y': 2, 'z': 3, 't': [1, 2, 3]},
        'd': {1, 2, 3},
    }, on_change=increment_counter)
    data['a'] = 42
    assert count == 1
    data['b'].append(4)
    assert count == 2
    data['b'][3].update(t=4)
    assert count == 3
    data['c']['x'] = 2
    assert count == 4
    data['c']['t'].append(4)
    assert count == 5
    data['d'].add(4)
    assert count == 6


def test_resolve_expect_args_once(monkeypatch: pytest.MonkeyPatch):
    introspection_count = 0
    original = helpers.expects_arguments

    def counting_expects_arguments(func):
        nonlocal introspection_count
        introspection_count += 1
        return original(func)

    monkeypatch.setattr(helpers, 'expects_arguments', counting_expects_arguments)

    received: list[ObservableChangeEventArguments] = []

    def no_arg_handler():
        ...

    def arg_handler(arguments):
        received.append(arguments)

    # Registration resolves `expects_arguments` exactly once per handler.
    data = ObservableDict({
        'b': [1, 2, 3, {'x': 1}],
        'c': {'t': [1, 2, 3]},
    }, on_change=no_arg_handler)
    data.on_change(arg_handler)
    assert introspection_count == 2

    # Firing the change (including nested mutations that walk the parent chain) must not introspect again.
    introspection_count = 0
    data['a'] = 42
    data['b'].append(4)
    data['b'][3]['x'] = 2
    data['c']['t'].append(4)
    assert introspection_count == 0

    # The arg-expecting handler still receives the change arguments; the no-arg handler is still called.
    assert len(received) == 4
    assert all(isinstance(arguments, ObservableChangeEventArguments) for arguments in received)
    assert received[0].sender is data


def test_async_handler(screen: Screen):
    reset_counter()
    data = ObservableList(on_change=increment_counter_slowly)

    @ui.page('/')
    def page():
        ui.button('Append 42', on_click=lambda: data.append(42))

    screen.open('/')
    assert count == 0

    screen.click('Append 42')
    screen.wait(0.5)
    assert count == 1


def test_setting_change_handler():
    reset_counter()
    data = ObservableList()
    data.append(1)
    assert count == 0

    data.on_change(increment_counter)
    data.append(2)
    assert count == 1


def test_copy():
    a = ObservableList([[1, 2, 3], [4, 5, 6]])
    b = copy.copy(a)
    c = copy.deepcopy(a)
    a.append([7, 8, 9])
    a[0][0] = 0

    assert a == [[0, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert b == [[0, 2, 3], [4, 5, 6]]
    assert c == [[1, 2, 3], [4, 5, 6]]


async def test_no_infinite_recursion(user: User):
    @ui.page('/')
    def page():
        list_ = ObservableList([1, 2, 3])
        list_ += list_
        ui.label(str(list_))

    await user.open('/')
    await user.should_see('[1, 2, 3, 1, 2, 3]')
