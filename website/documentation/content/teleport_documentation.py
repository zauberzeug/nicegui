from nicegui import ui

from . import doc


@doc.demo(ui.teleport)
def main_demo() -> None:
    from nicegui import ui

    ui.input.default_classes('inline-flex').default_props('dense outlined')

    md = ui.markdown('This is **input1:**.This is **input2:**.')

    def inject_inputs() -> None:
        id = f'c{md.id}'
        with ui.teleport(f'#{id} > p > strong:nth-child(1)'):
            ui.input(label='input1')

        with ui.teleport(f'#{id} > p > strong:nth-child(2)'):
            ui.input(label='input2')

    ui.button('inject inputs', on_click=inject_inputs)


doc.reference(ui.teleport)
