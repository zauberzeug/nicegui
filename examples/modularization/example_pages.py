import theme

from nicegui import ui


def create() -> None:

    @theme.page('/a', '- Example A -')
    def example_page():
        ui.label('Example A').classes('text-h4 text-grey-8')

    @theme.page('/b', '- Example B -')
    def example_page():
        ui.label('Example B').classes('text-h4 text-grey-8')

    @theme.page('/c', '- Example C -')
    def example_page():
        ui.label('Example C').classes('text-h4 text-grey-8')
