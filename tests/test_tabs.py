from nicegui import ui
from nicegui.testing import Screen


def test_with_strings(screen: Screen):
    @ui.page('/')
    def page():
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


def test_with_tab_objects(screen: Screen):
    event_tabs = []
    event_tab_panels = []

    @ui.page('/')
    def page():
        with ui.tabs(on_change=lambda e: event_tabs.append(e.value)) as tabs:
            tab1 = ui.tab('One')
            tab2 = ui.tab('Two')

        with ui.tab_panels(tabs, value=tab2, on_change=lambda e: event_tab_panels.append(e.value)) as tab_panels:
            with ui.tab_panel(tab1):
                ui.label('First tab')
            with ui.tab_panel(tab2):
                ui.label('Second tab')

        ui.button('Change tab_panels to Two', on_click=lambda: tab_panels.set_value(tab2))

    screen.open('/')
    screen.should_contain('One')
    screen.should_contain('Two')
    screen.should_contain('Second tab')
    screen.click('One')
    screen.should_contain('First tab')
    screen.click('Change tab_panels to Two')
    screen.should_contain('Second tab')
    assert event_tabs == ['Two', 'One', 'Two']
    assert event_tab_panels == ['One', 'Two']
