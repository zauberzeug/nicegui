from nicegui import ui

from . import doc


@doc.demo(ui.joystick)
def main_demo() -> None:
    ui.joystick(
        color='blue', size=50,
        on_move=lambda e: coordinates.set_text(f'{e.x:.3f}, {e.y:.3f}'),
        on_end=lambda _: coordinates.set_text('0, 0'),
    ).classes('bg-slate-300')
    coordinates = ui.label('0, 0')


doc.reference(ui.joystick)
