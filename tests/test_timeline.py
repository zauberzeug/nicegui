from nicegui import ui
from nicegui.testing import Screen


def test_timeline(screen: Screen):
    with ui.timeline():
        ui.timeline_entry('Entry 1', title='Title 1', subtitle='Subtitle 1')
        with ui.timeline():
            ui.label('Entry 2')

    screen.open('/')
    screen.should_contain('Entry 1')
    screen.should_contain('Title 1')
    screen.should_contain('Subtitle 1')
    screen.should_contain('Entry 2')
