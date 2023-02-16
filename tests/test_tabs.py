from nicegui import ui

from .screen import Screen


def test_tabs(screen: Screen):
    with ui.tabs() as tabs:
        ui.tab('One')
        ui.tab('Two')

    with ui.tab_panels(tabs, value='One'):
        with ui.tab_panel('One'):
            ui.label('First tab')
        with ui.tab_panel('Two'):
            ui.label('Second tab')

    screen.open('/')
    screen.should_contain('First tab')
    screen.click('Two')
    screen.should_contain('Second tab')
