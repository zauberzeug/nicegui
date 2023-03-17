from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen

columns = [
    {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True},
    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
]

rows = [
    {'id': 0, 'name': 'Alice', 'age': 18},
    {'id': 1, 'name': 'Bob', 'age': 21},
    {'id': 2, 'name': 'Lionel', 'age': 19},
]


def test_table(screen: Screen):
    ui.table(title='My Team', columns=columns, rows=rows)

    screen.open('/')
    screen.should_contain('My Team')
    screen.should_contain('Name')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Lionel')


def test_pagination(screen: Screen):
    ui.table(columns=columns, rows=rows, pagination=2)

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_not_contain('Lionel')
    screen.should_contain('1-2 of 3')


def test_filter(screen: Screen):
    table = ui.table(columns=columns, rows=rows)
    ui.input('Search by name').bind_value(table, 'filter')

    screen.open('/')
    screen.should_contain('Alice')
    screen.should_contain('Bob')
    screen.should_contain('Lionel')

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Search by name"]')
    element.send_keys('e')
    screen.should_contain('Alice')
    screen.should_not_contain('Bob')
    screen.should_contain('Lionel')


def test_add_remove(screen: Screen):
    table = ui.table(columns=columns, rows=rows)
    ui.button('Add', on_click=lambda: table.add_rows({'id': 3, 'name': 'Carol', 'age': 32}))
    ui.button('Remove', on_click=lambda: table.remove_rows(table.rows[0]))

    screen.open('/')
    screen.click('Add')
    screen.should_contain('Carol')

    screen.click('Remove')
    screen.should_not_contain('Alice')


def test_slot(screen: Screen):
    with ui.table(columns=columns, rows=rows, pagination=None) as table:
        with table.add_slot('top-row'):
            with table.row():
                with table.cell():
                    ui.label('This is top slot.')
        table.add_slot('body', '''
        <q-tr :props="props">
          <q-td key="name" :props="props">overriden</q-td>
          <q-td key="age" :props="props">
            <q-badge color="green">
              {{ props.row.age }}
            </q-badge>
          </q-td>
        </q-tr>
        ''')

    screen.open('/')
    screen.should_contain('This is top slot.')
    screen.should_not_contain('Alice')
    screen.should_contain('overriden')
    screen.should_contain('21')
