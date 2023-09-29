from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    with ui.element('div').classes('p-2 bg-blue-100'):
        ui.label('inside a colored div')


def more() -> None:
    @text_demo('Move elements', '''
        This demo shows how to move elements between or within containers.
    ''')
    def move_elements() -> None:
        with ui.card() as a:
            ui.label('A')
            x = ui.label('X')

        with ui.card() as b:
            ui.label('B')

        ui.button('Move X to A', on_click=lambda: x.move(a))
        ui.button('Move X to B', on_click=lambda: x.move(b))
        ui.button('Move X to top', on_click=lambda: x.move(target_index=0))

    @text_demo('Default props', '''
        You can set default props for all elements of a certain class.
        This way you can avoid repeating the same props over and over again.
    ''')
    def default_props() -> None:
        ui.button.default_props('rounded outline')
        ui.button('Button A')
        ui.button('Button B')
        ui.input()
        # END OF DEMO
        ui.button.default_props(remove='rounded outline')
