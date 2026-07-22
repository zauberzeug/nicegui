import asyncio
import copy
import gc
import pickle
import weakref

import pytest

from nicegui import ui
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


def test_rebuilding_list_in_place_does_not_accumulate_handlers():
    reset_counter()
    data = ObservableList([{}], on_change=increment_counter)
    for _ in range(3):
        data[:] = list(data)
    assert count == 3
    data[0]['x'] = 1
    assert count == 4, 'mutating a surviving item should fire exactly one change event'


def test_replacing_list_does_not_accumulate_handlers():
    reset_counter()
    data = ObservableDict({'items': [{}]}, on_change=increment_counter)
    for _ in range(3):
        data['items'] = list(data['items'])
    assert count == 3
    data['items'][0]['x'] = 1
    assert count == 4, 'mutating a surviving item should fire exactly one change event'


def test_removed_dict_values_are_detached():
    reset_counter()
    data = ObservableDict({'a': {}, 'b': {}, 'c': {}, 'd': {}}, on_change=increment_counter)
    detached = [data.pop('a'), data.popitem()[1], data['b'], data['c']]
    del data['b']
    data['c'] = {'new': True}
    data.update(e={})
    detached.append(data['e'])
    data.update(e={})
    n = count
    for item in detached:
        item['x'] = 1
    assert count == n, 'detached items should not fire change events anymore'
    data['c']['x'] = 1
    assert count == n + 1, 'items which are still contained should fire change events'
    item = data['c']
    data.clear()
    item['y'] = 2
    assert count == n + 2, 'items removed by clearing the dict should not fire change events anymore'


def test_removed_list_items_are_detached():
    reset_counter()
    data = ObservableList([{}, {}, {}, {}, {}, {}, {}], on_change=increment_counter)
    detached = [data.pop(), data[0], data[1], data[2], *data[3:5]]
    data.remove(data[0])
    del data[0]
    data[0] = {'new': True}
    del data[1:3]
    data.clear()
    n = count
    for item in detached:
        item['x'] = 1
    assert count == n, 'detached items should not fire change events anymore'


def test_multiplying_list_in_place():
    reset_counter()
    data = ObservableList([{}], on_change=increment_counter)
    item = data[0]
    data *= 2
    assert count == 1
    item['x'] = 1
    assert count == 2, 'items contained multiple times should fire only one change event'
    data *= 0
    assert count == 3
    item['y'] = 2
    assert count == 3, 'items removed by multiplying with zero should not fire change events anymore'


def test_items_contained_multiple_times_are_detached_on_last_removal():
    reset_counter()
    data = ObservableList(on_change=increment_counter)
    item = ObservableDict()
    data.append(item)
    data.append(item)
    item['x'] = 1
    assert count == 3, 'items contained multiple times should fire only one change event'
    data.pop()
    item['y'] = 2
    assert count == 5, 'items which are still contained once should fire change events'
    data.pop()
    item['z'] = 3
    assert count == 6, 'items removed completely should not fire change events anymore'


def test_items_shared_between_collections():
    counts = {'a': 0, 'b': 0}
    item = ObservableDict()
    a = ObservableList([item], on_change=lambda: counts.update(a=counts['a'] + 1))
    b = ObservableList([item], on_change=lambda: counts.update(b=counts['b'] + 1))
    item['x'] = 1
    assert counts == {'a': 1, 'b': 1}
    a.clear()
    item['y'] = 2
    assert counts == {'a': 2, 'b': 2}, 'item should only notify the collection which still contains it'
    assert b == [item]


def test_discarded_collections_are_garbage_collected():
    data = ObservableDict({'items': [{}]})
    refs = [weakref.ref(data['items'])]
    for _ in range(3):
        data['items'] = list(data['items'])
        refs.append(weakref.ref(data['items']))
    child = data['items'][0]
    del data
    gc.collect()
    assert [ref() for ref in refs] == [None, None, None, None], 'discarded collections should be garbage-collected'
    assert child == {}


def test_nested_observables_are_picklable():
    reset_counter()
    data = ObservableList([{'id': 1, 'tags': ['a', 'b']}, {'id': 2}])
    restored = pickle.loads(pickle.dumps(data))
    assert restored == [{'id': 1, 'tags': ['a', 'b']}, {'id': 2}]
    assert isinstance(restored, ObservableList)
    assert isinstance(restored[0], ObservableDict)
    assert isinstance(restored[0]['tags'], ObservableList)
    root = ObservableList(restored, on_change=increment_counter)
    root[0]['x'] = 1
    assert count == 1, 'a restored tree should wire up freshly and notify exactly once'


def test_pop_missing_key_raises_keyerror():
    reset_counter()
    data = ObservableDict({'a': 1}, on_change=increment_counter)
    with pytest.raises(KeyError):
        data.pop('missing')  # like dict.pop, a missing key without default raises
    assert count == 0, 'a failed pop must not fire a change event'
    assert data.pop('missing', 'default') == 'default'
    assert count == 0, 'popping a missing key with a default must not fire a change event'
    assert data.pop('a') == 1
    assert count == 1, 'popping an existing key fires exactly one change event'
    assert data.pop('a', None) is None, 'the default is returned when the key is gone'
    assert count == 1, 'popping a now-missing key with a default must not fire another change event'
