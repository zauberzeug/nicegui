from nicegui import ui

from .screen import Screen


def test_ui_startup_called_on_index_page(screen: Screen):
    label = ui.label('starting')
    ui.on_startup(lambda: label.set_text('started'))

    screen.open('/')
    screen.should_contain('started')


def test_ui_startup_called_on_shared_page(screen: Screen):
    @ui.page('/', shared=True)
    def shared_page():
        label = ui.label('starting')
        ui.on_startup(lambda: label.set_text('started'))

    screen.open('/')
    screen.should_contain('started')


def test_ui_startup_called_on_individual_page(screen: Screen):
    @ui.page('/')
    def individual_page():
        label = ui.label('starting')
        ui.on_startup(lambda: label.set_text('started'))

    screen.open('/')
    screen.should_contain('started')
