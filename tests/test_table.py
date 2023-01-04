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


def test_add_row(screen: Screen):
    table = ui.table({
        'columnDefs': [{'field': 'name'}, {'field': 'age'}],
        'rowData': [],
    })
    ui.button('Update', on_click=table.update)

    screen.open('/')
    table.options['rowData'].append({'name': 'Alice', 'age': 18})
    screen.click('Update')
    screen.should_contain('Alice')
    screen.should_contain('18')
    table.options['rowData'].append({'name': 'Bob', 'age': 21})
    screen.click('Update')
    screen.should_contain('Alice')
    screen.should_contain('18')
    screen.should_contain('Bob')
    screen.should_contain('21')


def test_click_cell(screen: Screen):
    table = ui.table({
        'columnDefs': [{'field': 'name'}, {'field': 'age'}],
        'rowData': [{'name': 'Alice', 'age': 18}],
    })
    table.on('cellClicked', lambda msg: ui.label(f'{msg["args"]["data"]["name"]} has been clicked!'))

    screen.open('/')
    screen.click('Alice')
    screen.should_contain('Alice has been clicked!')


def test_html_columns(screen: Screen):
    ui.table({
        'columnDefs': [{'field': 'name'}, {'field': 'age'}],
        'rowData': [{'name': '<span class="text-bold">Alice</span>', 'age': 18}],
    }, html_columns=[0])

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_not_contain('<span')
    assert 'text-bold' in screen.find('Alice').get_attribute('class')
