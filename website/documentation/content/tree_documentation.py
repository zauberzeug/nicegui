from nicegui import ui

from . import doc


@doc.demo(ui.tree)
def main_demo() -> None:
    ui.tree([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ], label_key='id', on_select=lambda e: ui.notify(e.value))


@doc.demo('Tree with custom header and body', '''
    Scoped slots can be used to insert custom content into the header and body of a tree node.
    See the [Quasar documentation](https://quasar.dev/vue-components/tree#customize-content) for more information.
''')
def tree_with_custom_header_and_body():
    tree = ui.tree([
        {'id': 'numbers', 'description': 'Just some numbers', 'children': [
            {'id': '1', 'description': 'The first number'},
            {'id': '2', 'description': 'The second number'},
        ]},
        {'id': 'letters', 'description': 'Some latin letters', 'children': [
            {'id': 'A', 'description': 'The first letter'},
            {'id': 'B', 'description': 'The second letter'},
        ]},
    ], label_key='id', on_select=lambda e: ui.notify(e.value))

    tree.add_slot('default-header', '''
        <span :props="props">Node <strong>{{ props.node.id }}</strong></span>
    ''')
    tree.add_slot('default-body', '''
        <span :props="props">Description: "{{ props.node.description }}"</span>
    ''')


@doc.demo('Expand and collapse programmatically', '''
    The whole tree or individual nodes can be toggled programmatically using the `expand()` and `collapse()` methods.
    This even works if a node is disabled (e.g. not clickable by the user).
''')
def expand_programmatically():
    t = ui.tree([
        {'id': 'A', 'children': [{'id': 'A1'}, {'id': 'A2'}], 'disabled': True},
        {'id': 'B', 'children': [{'id': 'B1'}, {'id': 'B2'}]},
    ], label_key='id').expand()

    with ui.row():
        ui.button('+ all', on_click=t.expand)
        ui.button('- all', on_click=t.collapse)
        ui.button('+ A', on_click=lambda: t.expand(['A']))
        ui.button('- A', on_click=lambda: t.collapse(['A']))


@doc.demo('Tree with checkboxes', '''
    The tree can be used with checkboxes by setting the "tick-strategy" prop.
''')
def tree_with_checkboxes():
    ui.tree([
        {'id': 'A', 'children': [{'id': 'A1'}, {'id': 'A2'}]},
        {'id': 'B', 'children': [{'id': 'B1'}, {'id': 'B2'}]},
    ], label_key='id', tick_strategy='leaf', on_tick=lambda e: ui.notify(e.value))


@doc.demo('Select/deselect or tick/untick programmatically', '''
    Node label in tree can be selected or deselected with the `select()` and `deselect()` methods.
    If enabled with "tick-strategy" prop then nodes can be ticked or unticked with the `tick()` and `untick()` methods.
''')
def select_or_tick_programmatically():
    with ui.row():
        t = ui.tree([
            {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
            {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
        ], label_key='id', tick_strategy='leaf').expand()
        with ui.column():
            ui.button('Tick 1, 2 & B', on_click=lambda: t.tick(['1', '2', 'B']))
            ui.button('Untick 2 & B', on_click=lambda: t.untick(['2', 'B']))
            ui.button('Tick all', on_click=t.tick)
            ui.button('Untick all', on_click=t.untick)
    with ui.row():
        ui.button('Select A', on_click=lambda: t.select('A'))
        ui.button('Deselect A', on_click=t.deselect)


doc.reference(ui.tree)
