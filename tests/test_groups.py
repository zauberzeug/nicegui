from nicegui import ui

from .screen import Screen


def test_remove_and_clear(screen: Screen):
    with ui.row() as row:
        ui.label('Label A')
        b = ui.label('Label B')
        ui.label('Label C')

    ui.button('Remove B', on_click=lambda: row.remove(b))
    ui.button('Remove 0', on_click=lambda: row.remove(0))
    ui.button('Clear', on_click=lambda: row.clear())

    screen.open('/')
    screen.should_contain('Label A')
    screen.should_contain('Label B')
    screen.should_contain('Label C')

    screen.click('Remove B')
    screen.should_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_contain('Label C')

    screen.click('Remove 0')
    screen.should_not_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_contain('Label C')

    screen.click('Clear')
    screen.should_not_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_not_contain('Label C')
