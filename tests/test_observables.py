import asyncio
import sys

from nicegui import ui
from nicegui.observables import ObservableDict, ObservableList, ObservableSet
from nicegui.testing import Screen

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
    if sys.version_info >= (3, 9):
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


def test_async_handler(screen: Screen):
    reset_counter()
    data = ObservableList(on_change=increment_counter_slowly)
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
