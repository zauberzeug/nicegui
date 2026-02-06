from nicegui import ui
from nicegui.testing import SharedScreen


def test_with_strings(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.should_contain('First tab')
    shared_screen.click('Two')
    shared_screen.should_contain('Second tab')


def test_with_tab_objects(shared_screen: SharedScreen):
    tab_events = []
    tab_panel_events = []

    @ui.page('/')
    def page():
        with ui.tabs(on_change=lambda e: tab_events.append(e.value)) as tabs:
            tab1 = ui.tab('One')
            tab2 = ui.tab('Two')

        with ui.tab_panels(tabs, value=tab2, on_change=lambda e: tab_panel_events.append(e.value)) as tab_panels:
            with ui.tab_panel(tab1):
                ui.label('First tab')
            with ui.tab_panel(tab2):
                ui.label('Second tab')

        ui.button('Switch to Two', on_click=lambda: tab_panels.set_value(tab2))

    shared_screen.open('/')
    shared_screen.should_contain('One')
    shared_screen.should_contain('Two')
    shared_screen.should_contain('Second tab')
    assert tab_events == ['Two']
    assert tab_panel_events == []

    shared_screen.click('One')
    shared_screen.should_contain('First tab')
    assert tab_events == ['Two', 'One']
    assert tab_panel_events == ['One']

    shared_screen.click('Switch to Two')
    shared_screen.should_contain('Second tab')
    assert tab_events == ['Two', 'One', 'Two']
    assert tab_panel_events == ['One', 'Two']


def test_updating_offscreen_elements_with_update_method(shared_screen: SharedScreen):
    @ui.page('/')
    def main_page():
        with ui.tabs() as tabs:
            ui.tab('One')
            ui.tab('Two')

        with ui.tab_panels(tabs, value='One'):
            with ui.tab_panel('One'):
                ui.button('Update', on_click=lambda: editor.update())
            with ui.tab_panel('Two'):
                editor = ui.json_editor({})

    shared_screen.open('/')
    shared_screen.click('Update')
