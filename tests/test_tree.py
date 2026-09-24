from nicegui import ui
from nicegui.testing import Screen, User


def test_tree(screen: Screen):
    @ui.page('/')
    def page():
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
    @ui.page('/')
    def page():
        tree = ui.tree([
            {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
            {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
        ], label_key='id')

        ui.button('Select', on_click=lambda: tree.select('2'))
        ui.button('Deselect', on_click=tree.deselect)
        ui.label().bind_text_from(tree.props, 'selected', lambda x: f'Selected: {x}')

    screen.open('/')
    screen.click('Select')
    screen.should_contain('Selected: 2')

    screen.click('Deselect')
    screen.should_contain('Selected: None')


def test_tick_untick_node_or_nodes(screen: Screen):
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

    screen.open('/')
    screen.should_contain('Ticked: []')

    screen.click('Tick some')
    screen.should_contain("Ticked: ['1', '2', 'B']")

    screen.click('Untick some')
    screen.should_contain("Ticked: ['2']")

    screen.click('Tick all')
    screen.should_contain("Ticked: ['1', '2', 'A', 'B', 'letters', 'numbers']")

    screen.click('Untick all')
    screen.should_contain('Ticked: []')


def test_filter(screen: Screen):
    @ui.page('/')
    def page():
        t = ui.tree([
            {'id': 'fruits', 'children': [{'id': 'Apple'}, {'id': 'Banana'}, {'id': 'Cherry'}]},
        ], label_key='id', tick_strategy='leaf-filtered').expand()
        ui.button('Filter', on_click=lambda: t.set_filter('a'))
        ui.label().bind_text_from(t.props, 'filter', lambda x: f'Filter: {x}')

    screen.open('/')
    screen.should_contain('Apple')
    screen.should_contain('Banana')
    screen.should_contain('Cherry')

    screen.click('Filter')
    screen.should_contain('Filter: a')
    screen.should_contain('Apple')
    screen.should_contain('Banana')
    screen.should_not_contain('Cherry')


async def test_nodes_visibility(user: User):
    trees: dict[str, ui.tree] = {}

    @ui.page('/')
    def page():
        trees['expanded'] = ui.tree([{'id': 'a', 'children': [{'id': 'b'}]}], label_key='id').expand(['a'])
        trees['collapsed'] = ui.tree([{'id': 'a', 'children': [{'id': 'b'}]}], label_key='id').collapse()
        trees['deep'] = ui.tree([{'id': 'A', 'children': [{'id': 'B', 'children': [{'id': 'C'}]}]}],
                                label_key='id').expand(['B'])

    await user.open('/')

    def ids(tree: ui.tree, *, visible: bool) -> list[str]:
        return [node['id'] for node in tree.nodes(visible=visible)]

    assert ids(trees['expanded'], visible=False) == []
    assert ids(trees['collapsed'], visible=False) == ['b']
    assert ids(trees['deep'], visible=False) == ['B', 'C']

    assert ids(trees['expanded'], visible=True) == ['a', 'b']
    assert ids(trees['collapsed'], visible=True) == ['a']
    assert ids(trees['deep'], visible=True) == ['A']
