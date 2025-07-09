from nicegui import ui

from . import doc


@doc.demo(ui.fab)
def main_demo() -> None:
    with ui.fab('navigation', label='Transport'):
        ui.fab_action('train', on_click=lambda: ui.notify('Train'))
        ui.fab_action('sailing', on_click=lambda: ui.notify('Boat'))
        ui.fab_action('rocket', on_click=lambda: ui.notify('Rocket'))


@doc.demo('Styling', '''
    You can style the FAB and its actions using the `color` parameter.
    The `color` parameter accepts a Quasar color, a Tailwind color, or a CSS color.
    You can also change the direction of the FAB using the `direction` parameter.
''')
def styling_demo() -> None:
    with ui.fab('shopping_cart', label='Shop', color='teal', direction='up') \
            .classes('mt-40 mx-auto'):
        ui.fab_action('sym_o_nutrition', label='Fruits', color='green')
        ui.fab_action('local_pizza', label='Pizza', color='yellow')
        ui.fab_action('sym_o_icecream', label='Ice Cream', color='orange')


doc.reference(ui.fab, title='Reference for ui.fab')
doc.reference(ui.fab_action, title='Reference for ui.fab_action')
