from nicegui import ui
from . import svg

def create() -> None:
    # Create UI components
    with ui.row().style('filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1))'):
        with ui.card().style(r'clip-path: polygon(0 0, 100% 0, 100% 90%, 0 100%)').classes('pb-16 no-shadow'), ui.row().classes('no-wrap'):
            # First column
            with ui.column().classes('items-center'):
                svg.face().classes('w-16 mx-6 stroke-black dark:stroke-gray-100 stroke-2').on('click', handle_face_click)
                create_first_column_ui()

            # Second column
            with ui.column().classes('items-center'):
                create_second_column_ui()

def create_first_column_ui() -> None:
    # Create UI elements for the first column
    ui.button('Click me!', on_click=handle_button_click).classes('w-full')
    ui.input('Text', value='abc', on_change=handle_input_change)
    ui.checkbox('Check', on_change=handle_checkbox_change)
    ui.switch('Switch', on_change=handle_switch_change)

def create_second_column_ui() -> None:
    # Create UI elements for the second column
    output = ui.label('Try it out!').classes(
        'w-44 my-6 h-8 text-xl text-gray-800 dark:text-gray-200 overflow-hidden text-ellipsis text-center')
    ui.slider(min=0, max=100, value=50, step=0.1, on_change=handle_slider_change).style('width: 150px; margin-bottom: 2px')

    with ui.row():
        ui.number('Number', value=3.1415927, format='%.2f', on_change=handle_number_change).classes('w-20')
        ui.select({1: 'One', 2: 'Two', 3: 'Three'}, value=1, on_change=handle_select_change)

    ui.toggle(['1', '2', '3'], value='1', on_change=handle_toggle_change)
    ui.radio(['A', 'B', 'C'], value='A', on_change=handle_radio_change).props('inline')

def handle_face_click(_) -> None:
    output.set_text("That's my face!")

def handle_button_click() -> None:
    output.set_text('Clicked')

def handle_input_change(e) -> None:
    output.set_text(e.value)

def handle_checkbox_change(e) -> None:
    output.set_text('Checked' if e.value else 'Unchecked')

def handle_switch_change(e) -> None:
    output.set_text('Switched on' if e.value else 'Switched off')

def handle_slider_change(e) -> None:
    output.set_text(e.value)

def handle_number_change(e) -> None:
    output.set_text(e.value)

def handle_select_change(e) -> None:
    output.set_text(e.value)

def handle_toggle_change(e) -> None:
    output.set_text(e.value)

def handle_radio_change(e) -> None:
    output.set_text(e.value)

