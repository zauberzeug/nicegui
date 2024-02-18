from nicegui import ui

from . import doc


@doc.demo(ui.stepper)
def main_demo() -> None:
    with ui.stepper().props('vertical').classes('w-full') as stepper:
        with ui.step('Preheat'):
            ui.label('Preheat the oven to 350 degrees')
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
        with ui.step('Ingredients'):
            ui.label('Mix the ingredients')
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
                ui.button('Back', on_click=stepper.previous).props('flat')
        with ui.step('Bake'):
            ui.label('Bake for 20 minutes')
            with ui.stepper_navigation():
                ui.button('Done', on_click=lambda: ui.notify('Yay!', type='positive'))
                ui.button('Back', on_click=stepper.previous).props('flat')


doc.reference(ui.stepper)
