from nicegui import ui
from nicegui.testing import SharedScreen


def test_tree(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.tree([
            {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
            {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
        ], label_key='id')

    shared_screen.open('/')
    shared_screen.should_contain('numbers')
    shared_screen.should_contain('letters')
    shared_screen.should_not_contain('1')
    shared_screen.should_not_contain('2')
    shared_screen.should_not_contain('A')
    shared_screen.should_not_contain('B')

    shared_screen.find_by_class('q-icon').click()
    shared_screen.wait(0.5)
    shared_screen.should_contain('1')
    shared_screen.should_contain('2')


def test_expand_and_collapse_nodes(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        tree = ui.tree([
            {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
            {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
        ], label_key='id')

        ui.button('Expand all', on_click=tree.expand)
        ui.button('Collapse all', on_click=tree.collapse)
        ui.button('Expand numbers', on_click=lambda: tree.expand(['numbers']))
        ui.button('Collapse numbers', on_click=lambda: tree.collapse(['numbers']))

    shared_screen.open('/')
    shared_screen.click('Expand all')
    shared_screen.wait(0.5)
    shared_screen.should_contain('1')
    shared_screen.should_contain('2')
    shared_screen.should_contain('A')
    shared_screen.should_contain('B')

    shared_screen.click('Collapse all')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('1')
    shared_screen.should_not_contain('2')
    shared_screen.should_not_contain('A')
    shared_screen.should_not_contain('B')

    shared_screen.click('Expand numbers')
    shared_screen.wait(0.5)
    shared_screen.should_contain('1')
    shared_screen.should_contain('2')
    shared_screen.should_not_contain('A')
    shared_screen.should_not_contain('B')

    shared_screen.click('Expand all')
    shared_screen.click('Collapse numbers')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('1')
    shared_screen.should_not_contain('2')
    shared_screen.should_contain('A')
    shared_screen.should_contain('B')


def test_select_deselect_node(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        tree = ui.tree([
            {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
            {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
        ], label_key='id')

        ui.button('Select', on_click=lambda: tree.select('2'))
        ui.button('Deselect', on_click=tree.deselect)
        ui.label().bind_text_from(tree.props, 'selected', lambda x: f'Selected: {x}')

    shared_screen.open('/')
    shared_screen.click('Select')
    shared_screen.should_contain('Selected: 2')

    shared_screen.click('Deselect')
    shared_screen.should_contain('Selected: None')


def test_tick_untick_node_or_nodes(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        tree = ui.tree([
            {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
            {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
        ], label_key='id', tick_strategy='leaf')

        ui.button('Tick some', on_click=lambda: tree.tick(['1', '2', 'B']))
        ui.button('Untick some', on_click=lambda: tree.untick(['1', 'B']))
        ui.button('Tick all', on_click=tree.tick)
        ui.button('Untick all', on_click=tree.untick)
        ui.label().bind_text_from(tree.props, 'ticked', lambda x: f'Ticked: {sorted(x)}')

    shared_screen.open('/')
    shared_screen.should_contain('Ticked: []')

    shared_screen.click('Tick some')
    shared_screen.should_contain("Ticked: ['1', '2', 'B']")

    shared_screen.click('Untick some')
    shared_screen.should_contain("Ticked: ['2']")

    shared_screen.click('Tick all')
    shared_screen.should_contain("Ticked: ['1', '2', 'A', 'B', 'letters', 'numbers']")

    shared_screen.click('Untick all')
    shared_screen.should_contain('Ticked: []')


def test_filter(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        t = ui.tree([
            {'id': 'fruits', 'children': [{'id': 'Apple'}, {'id': 'Banana'}, {'id': 'Cherry'}]},
        ], label_key='id', tick_strategy='leaf-filtered').expand()
        ui.button('Filter', on_click=lambda: t.set_filter('a'))

    shared_screen.open('/')
    shared_screen.should_contain('Apple')
    shared_screen.should_contain('Banana')
    shared_screen.should_contain('Cherry')

    shared_screen.click('Filter')
    shared_screen.should_contain('Apple')
    shared_screen.should_contain('Banana')
    shared_screen.should_not_contain('Cherry')
