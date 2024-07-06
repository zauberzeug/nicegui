from nicegui import ui
from nicegui.testing import Screen


def test_stepper(screen: Screen):
    with ui.stepper() as stepper:
        with ui.step('One'):
            ui.label('First step')
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
                ui.button('Back', on_click=stepper.previous)
        with ui.step('Two'):
            ui.label('Second step')
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
                ui.button('Back', on_click=stepper.previous)

    screen.open('/')
    screen.should_contain('First step')
    screen.should_not_contain('Second step')
    screen.click('Next')
    screen.should_contain('Second step')
    screen.should_not_contain('First step')
    screen.click('Back')
    screen.should_contain('First step')
    screen.should_not_contain('Second step')
