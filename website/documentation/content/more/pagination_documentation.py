from nicegui import ui

from ...model import UiElementDocumentation


class PaginationDocumentation(UiElementDocumentation, element=ui.pagination):

    def main_demo(self) -> None:
        p = ui.pagination(1, 5, direction_links=True)
        ui.label().bind_text_from(p, 'value', lambda v: f'Page {v}')
