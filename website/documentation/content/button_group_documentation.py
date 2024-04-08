from nicegui import ui

from . import doc


@doc.demo(ui.button_group)
def main_demo() -> None:
    with ui.button_group():
        ui.button('One', on_click=lambda: ui.notify('You clicked Button 1!'))
        ui.button('Two', on_click=lambda: ui.notify('You clicked Button 2!'))
        ui.button('Three', on_click=lambda: ui.notify('You clicked Button 3!'))


@doc.demo('Button group with dropdown button', '''
    You can also add a dropdown button to a button group.
''')
def with_dropdown() -> None:
    with ui.button_group():
        ui.button('One')
        ui.button('Two')
        with ui.dropdown_button('Dropdown'):
            with ui.list():
                ui.item('Item 1', on_click=lambda: ui.notify('Item 1'))
                ui.item('Item 2', on_click=lambda: ui.notify('Item 2'))


@doc.demo('Button group styling', '''
    You can apply the same styling options to a button group as to a button, like "flat", "outline", "push", ...
    However, you must always use the same design props for the button group and its containing buttons.
''')
def styling() -> None:
    with ui.button_group().props('rounded'):
        ui.button('One')
        ui.button('Two')
        ui.button('Three')
    with ui.button_group().props('push glossy'):
        ui.button('One', color='red').props('push')
        ui.button('Two', color='orange').props('push text-color=black')
        ui.button('Three', color='yellow').props('push text-color=black')
    with ui.button_group().props('outline'):
        ui.button('One').props('outline')
        ui.button('Two').props('outline')
        ui.button('Three').props('outline')


doc.reference(ui.button_group)
