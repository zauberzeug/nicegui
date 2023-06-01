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
    data[0] = 1
    assert count == 6
    data[0:2] = [1, 2, 3]
    assert count == 7
    del data[0]
    assert count == 8
    del data[0:1]
    assert count == 9
    data.clear()
    assert count == 10


def test_nested_observables():
    reset_counter()
    data = make_observable({
        'a': 1,
        'b': [1, 2, 3, {'x': 1, 'y': 2, 'z': 3}],
        'c': {'x': 1, 'y': 2, 'z': 3, 't': [1, 2, 3]},
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
