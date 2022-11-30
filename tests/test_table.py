from nicegui import ui

from .screen import Screen


def test_update_table(screen: Screen):
    table = ui.table({
        'columnDefs': [{'field': 'name'}, {'field': 'age'}],
        'rowData': [{'name': 'Alice', 'age': 18}],
    })

    screen.open('/')
    screen.should_contain('Name')
    screen.should_contain('Age')
    screen.should_contain('Alice')
    screen.should_contain('18')

    table.options['rowData'][0]['age'] = 42
    table.update()
    screen.should_contain('42')
