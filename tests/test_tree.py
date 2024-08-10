from nicegui import ui
from nicegui.testing import Screen


def test_tree(screen: Screen):
    ui.tree([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ], label_key='id')

    screen.open('/')
    screen.should_contain('numbers')
    screen.should_contain('letters')
    screen.should_not_contain('1')
    screen.should_not_contain('2')
    screen.should_not_contain('A')
    screen.should_not_contain('B')

    screen.find_by_class('q-icon').click()
    screen.wait(0.5)
    screen.should_contain('1')
    screen.should_contain('2')


def test_expand_and_collapse_nodes(screen: Screen):
    tree = ui.tree([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ], label_key='id')

    ui.button('Expand all', on_click=tree.expand)
    ui.button('Collapse all', on_click=tree.collapse)
    ui.button('Expand numbers', on_click=lambda: tree.expand(['numbers']))
    ui.button('Collapse numbers', on_click=lambda: tree.collapse(['numbers']))

    screen.open('/')
    screen.click('Expand all')
    screen.wait(0.5)
    screen.should_contain('1')
    screen.should_contain('2')
    screen.should_contain('A')
    screen.should_contain('B')

    screen.click('Collapse all')
    screen.wait(0.5)
    screen.should_not_contain('1')
    screen.should_not_contain('2')
    screen.should_not_contain('A')
    screen.should_not_contain('B')

    screen.click('Expand numbers')
    screen.wait(0.5)
    screen.should_contain('1')
    screen.should_contain('2')
    screen.should_not_contain('A')
    screen.should_not_contain('B')

    screen.click('Expand all')
    screen.click('Collapse numbers')
    screen.wait(0.5)
    screen.should_not_contain('1')
    screen.should_not_contain('2')
    screen.should_contain('A')
    screen.should_contain('B')


def test_select_deselect_node(screen: Screen):
    tree = ui.tree([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ], label_key='id')

    ui.button('Select number', on_click=lambda: tree.select('2'))
    ui.button('Deselect number', on_click=lambda: tree.deselect())

    screen.open('/')
    screen.click('Select number')
    assert tree._props['selected'] == '2'

    screen.click('Deselect number')
    assert tree._props['selected'] is None
