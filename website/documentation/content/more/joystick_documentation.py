from nicegui import ui

from ...model import UiElementDocumentation


class JoystickDocumentation(UiElementDocumentation, element=ui.joystick):

    def main_demo(self) -> None:
        ui.joystick(color='blue', size=50,
                    on_move=lambda e: coordinates.set_text(f"{e.x:.3f}, {e.y:.3f}"),
                    on_end=lambda _: coordinates.set_text('0, 0'))
        coordinates = ui.label('0, 0')
