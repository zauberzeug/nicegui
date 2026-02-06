from nicegui import ui
from nicegui.testing import SharedScreen


def test_splitter(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.splitter() as splitter:
            with splitter.before:
                ui.label('Left hand side.')
            with splitter.after:
                ui.label('Right hand side.')
        ui.label().bind_text_from(splitter, 'value')

    shared_screen.open('/')
    shared_screen.should_contain('Left hand side.')
    shared_screen.should_contain('Right hand side.')
    shared_screen.should_contain('50')
    # TODO: programmatically move splitter
