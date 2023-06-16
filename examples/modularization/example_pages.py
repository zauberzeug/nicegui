import theme

from nicegui import ui


def create() -> None:

    @ui.page('/a')
    def example_page_a():
        with theme.frame('- Example A -'):
            ui.label('Example A').classes('text-h4 text-grey-8')

    @ui.page('/b')
    def example_page_b():
        with theme.frame('- Example B -'):
            ui.label('Example B').classes('text-h4 text-grey-8')
