import sys

from nicegui.observables import make_observable

count = 0


def reset_counter():
    global count
    count = 0


def increment_counter():
    global count
    count += 1


def test_observable_dict():
    reset_counter()
    data = make_observable({}, increment_counter)
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
    data = make_observable([], increment_counter)
    data.append(1)
    assert count == 1
    data.extend([2, 3, 4])
    assert count == 2
    data.insert(0, 0)
    assert count == 3
    data.remove(1)
    assert count == 4
    data.pop()
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
    data = make_observable({1, 2, 3, 4, 5}, increment_counter)
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
    data = make_observable({
        'a': 1,
        'b': [1, 2, 3, {'x': 1, 'y': 2, 'z': 3}],
        'c': {'x': 1, 'y': 2, 'z': 3, 't': [1, 2, 3]},
        'd': {1, 2, 3},
    }, increment_counter)
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
