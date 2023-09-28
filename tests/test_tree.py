from nicegui import ui

from .screen import Screen


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
    screen.should_contain('1')
    screen.should_contain('2')


def test_default_expand_all(screen: Screen):
    ui.tree([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ], label_key='id', default_expand_all=True)

    screen.open('/')
    screen.should_contain('numbers')
    screen.should_contain('letters')
    screen.should_contain('1')
    screen.should_contain('2')
    screen.should_contain('A')
    screen.should_contain('B')
