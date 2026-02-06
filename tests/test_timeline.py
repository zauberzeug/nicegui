from nicegui import ui
from nicegui.testing import SharedScreen


def test_timeline(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.timeline():
            ui.timeline_entry('Entry 1', title='Title 1', subtitle='Subtitle 1')
            with ui.timeline():
                ui.label('Entry 2')

    shared_screen.open('/')
    shared_screen.should_contain('Entry 1')
    shared_screen.should_contain('Title 1')
    shared_screen.should_contain('Subtitle 1')
    shared_screen.should_contain('Entry 2')
