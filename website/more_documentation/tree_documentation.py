from typing import List

from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.tree([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ], label_key='id', on_select=lambda e: ui.notify(e.value))


def more() -> None:
    @text_demo('Tree with custom header and body', '''
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

    @text_demo('Expand programmatically', '''
               The tree can be expanded programmatically by modifying the `expanded` prop.
               ''')
    def expand_programmatically():
        def expand(node_ids: List[str]) -> None:
            t._props['expanded'] = node_ids
            t.update()

        with ui.row():
            ui.button('all', on_click=lambda: expand(['A', 'B']))
            ui.button('A', on_click=lambda: expand(['A']))
            ui.button('B', on_click=lambda: expand(['B']))
            ui.button('close', on_click=lambda: expand([]))

        t = ui.tree([
            {'id': 'A', 'children': [{'id': 'A1'}, {'id': 'A2'}]},
            {'id': 'B', 'children': [{'id': 'B1'}, {'id': 'B2'}]},
        ], label_key='id')
