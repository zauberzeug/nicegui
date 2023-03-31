from nicegui import ui

from .screen import Screen


def test_splitter(screen: Screen):
    with ui.splitter() as splitter:
        with splitter.add_slot('before'):
            ui.label('This is some content on the left hand side.')
        with splitter.add_slot('after'):
            ui.label('This is some content on the right hand side.')
    ui.label().bind_text_from(splitter, 'value')

    screen.open('/')
    screen.should_contain('50')
    screen.should_contain("This is some content on the left hand side.")
    screen.should_contain("This is some content on the right hand side.")
    # Not sure how to programmatically move splitter
    # screen.should_contain('70')
