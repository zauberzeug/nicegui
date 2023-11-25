from nicegui import ui

from ...model import UiElementDocumentation


class ColorsDocumentation(UiElementDocumentation, element=ui.colors):

    def main_demo(self) -> None:
        # ui.button('Default', on_click=lambda: ui.colors())
        # ui.button('Gray', on_click=lambda: ui.colors(primary='#555'))
        # END OF DEMO
        b1 = ui.button('Default', on_click=lambda: [b.classes(replace='!bg-primary') for b in [b1, b2]])
        b2 = ui.button('Gray', on_click=lambda: [b.classes(replace='!bg-[#555]') for b in [b1, b2]])
