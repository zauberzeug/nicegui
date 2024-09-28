from typing import Optional

from nicegui import ui
from nicegui.testing import Screen, User


def test_teleport(screen: Screen):
    ui.card().classes('card')

    def create_teleport():
        with ui.teleport('.card'):
            ui.label('Hello')

    ui.button('create', on_click=create_teleport)

    screen.open('/')
    screen.click('create')
    assert screen.find_by_css('.card > div').text == 'Hello'


def test_teleport_with_element(screen: Screen):
    card = ui.card().classes('card')

    def create_teleport():
        with ui.teleport(card):
            ui.label('Hello')

    ui.button('create', on_click=create_teleport)

    screen.open('/')
    screen.click('create')
    assert screen.find_by_css('.card > div').text == 'Hello'


def test_update(screen: Screen):
    teleport: Optional[ui.teleport] = None

    card = ui.card().classes('card')

    def create_teleport():
        nonlocal teleport
        with ui.teleport('.card') as teleport:
            ui.label('Hello')

    ui.button('create', on_click=create_teleport)

    def rebuild_card():
        card.delete()
        ui.card().classes('card')
        teleport.update()  # type: ignore

    ui.button('rebuild card', on_click=rebuild_card)

    screen.open('/')
    screen.click('create')
    screen.should_contain('Hello')
    screen.click('rebuild card')
    assert screen.find_by_css('.card > div').text == 'Hello'


async def test_teleport_to_cell(user: User):
    colors = ['red', 'green', 'blue']
    columns = [
        {'name': 'product', 'label': 'Product', 'field': 'product', 'align': 'center'},
        {'name': 'color', 'label': 'Color', 'field': 'color', 'align': 'center'},
    ]
    rows = [
        {'product': 'A', 'color': 'red'},
        {'product': 'B', 'color': 'green'},
        {'product': 'C', 'color': 'blue'},
    ]
    table = ui.table(columns=columns, rows=rows, row_key='product').classes('w-72')
    table.add_slot('body-cell-color', r'''<q-td key="color" :props="props"></q-td>''')
    for r, row in enumerate(rows):
        with ui.teleport(f'#c{table.id} tr:nth-child({r+1}) td:nth-child(2)'):
            ui.select(colors).bind_value(row, 'color').mark(f'row{r+1}')

    await user.open('/')
    user.find(kind=ui.select, marker='row1').elements.pop().set_value('green')
    assert rows == [
        {'product': 'A', 'color': 'green'},
        {'product': 'B', 'color': 'green'},
        {'product': 'C', 'color': 'blue'},
    ]
