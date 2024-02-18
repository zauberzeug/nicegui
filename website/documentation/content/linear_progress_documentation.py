from nicegui import ui

from . import doc


@doc.demo(ui.linear_progress)
def main_demo() -> None:
    slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
    ui.linear_progress().bind_value_from(slider, 'value')


doc.reference(ui.linear_progress)
