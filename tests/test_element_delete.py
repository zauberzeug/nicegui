from nicegui import ui

from .screen import Screen


def test_remove_element_by_reference(screen: Screen):
    with ui.row() as row:
        ui.label('Label A')
        b = ui.label('Label B')
        ui.label('Label C')

    ui.button('Remove', on_click=lambda: row.remove(b))

    screen.open('/')
    screen.click('Remove')
    screen.wait(0.5)
    screen.should_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_contain('Label C')
    assert b.is_deleted


def test_remove_element_by_index(screen: Screen):
    with ui.row() as row:
        ui.label('Label A')
        b = ui.label('Label B')
        ui.label('Label C')

    ui.button('Remove', on_click=lambda: row.remove(1))

    screen.open('/')
    screen.click('Remove')
    screen.wait(0.5)
    screen.should_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_contain('Label C')
    assert b.is_deleted


def test_clear(screen: Screen):
    with ui.row() as row:
        a = ui.label('Label A')
        b = ui.label('Label B')
        c = ui.label('Label C')

    ui.button('Clear', on_click=row.clear)

    screen.open('/')
    screen.click('Clear')
    screen.wait(0.5)
    screen.should_not_contain('Label A')
    screen.should_not_contain('Label B')
    screen.should_not_contain('Label C')
    assert a.is_deleted
    assert b.is_deleted
    assert c.is_deleted
