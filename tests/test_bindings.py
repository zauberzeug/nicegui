
from nicegui import ui

from .screen import Screen


def test_ui_select_with_tuple_as_key(screen: Screen):
    class Model():
        selection = None
    data = Model()
    options = {
        (2, 1): 'option A',
        (1, 2): 'option B',
    }
    data.selection = list(options.keys())[0]
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
    class Model():
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
    class Model():
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
