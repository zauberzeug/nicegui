from nicegui import ui


def create_content():
    with ui.column().classes('w-5/12'):
        ui.button('Click me!', on_click=lambda: output.set_text('Click!'))
        ui.checkbox('Check me!', on_change=lambda e: output.set_text('Checked.' if e.value else 'Unchecked.'))
        ui.switch('Switch me!', on_change=lambda e: output.set_text('Switched.' if e.value else 'Unswitched.'))
        ui.input('Text', value='abc', on_change=lambda e: output.set_text(e.value))
        ui.number('Number', value=3.1415927, format='%.2f', on_change=lambda e: output.set_text(e.value))

    with ui.column().classes('w-6/12'):
        ui.slider(min=0, max=100, value=50, step=0.1, on_change=lambda e: output.set_text(e.value))
        ui.radio(['A', 'B', 'C'], value='A', on_change=lambda e: output.set_text(e.value)).props('inline')
        ui.toggle(['1', '2', '3'], value='1', on_change=lambda e: output.set_text(e.value))
        ui.select({1: 'One', 2: 'Two', 3: 'Three'}, value=1, on_change=lambda e: output.set_text(e.value))

    output = ui.label('Try it out!').classes('mt-8 w-44 text-xl text-grey-9 overflow-hidden text-ellipsis')
