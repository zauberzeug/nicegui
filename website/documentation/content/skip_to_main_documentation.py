from nicegui import ui

from . import doc


@doc.auto_execute
@doc.demo(ui.skip_to_main)
def main_demo() -> None:
    @ui.page('/skip_to_main_demo')
    def skip_to_main_demo():
        ui.skip_to_main()
        ui.label('Press Tab to reveal the skip button, then Enter to jump here.')

    # @ui.page('/')
    def page():
        ui.link('show page with skip-to-main button', skip_to_main_demo)
    page()  # HIDE


@doc.auto_execute
@doc.demo('Custom content', '''
    Use ``ui.skip_to_main`` as a context manager to customize the button text and styling.
    The skip target will be set to the element created right after the context manager block.
''')
def custom_content_demo() -> None:
    @ui.page('/skip_to_main_custom_demo')
    def skip_to_main_custom_demo():
        with ui.skip_to_main().classes('bg-primary text-white p-2'), ui.row(align_items='center'):
            ui.icon('skip_next').classes('text-2xl')
            ui.label('Jump to main content')
        ui.label('Main content starts here')

    # @ui.page('/')
    def page():
        ui.link('show page with custom skip button', skip_to_main_custom_demo)
    page()  # HIDE


doc.reference(ui.skip_to_main)
