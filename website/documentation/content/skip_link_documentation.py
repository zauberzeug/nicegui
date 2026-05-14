from nicegui import ui

from . import doc


@doc.auto_execute
@doc.demo(ui.skip_link)
def main_demo() -> None:
    @ui.page('/skip_link_demo')
    def skip_link_demo():
        ui.button('Navigation 1')
        ui.button('Navigation 2')
        main = ui.label('Press Tab to reveal the skip link, then Enter to jump here.')
        ui.skip_link(target=main)

    # @ui.page('/')
    def page():
        ui.link('show page with skip link', skip_link_demo)
    page()  # HIDE


@doc.auto_execute
@doc.demo('Custom content', '''
    Pass a different ``text`` for a custom label, or use ``ui.skip_link`` as a context manager
    to insert arbitrary child content like icons.
''')
def custom_content_demo() -> None:
    @ui.page('/skip_link_custom_demo')
    def skip_link_custom_demo():
        ui.button('Navigation 1')
        with ui.column() as main:
            ui.label('Main content starts here')
        with ui.skip_link(text='', target=main).classes('bg-primary text-white p-2'), \
                ui.row(align_items='center'):
            ui.icon('skip_next').classes('text-2xl')
            ui.label('Jump to main content')

    # @ui.page('/')
    def page():
        ui.link('show page with custom skip link', skip_link_custom_demo)
    page()  # HIDE


doc.reference(ui.skip_link)
