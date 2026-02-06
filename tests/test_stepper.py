from nicegui import ui
from nicegui.testing import SharedScreen


def test_stepper(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
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

    shared_screen.open('/')
    shared_screen.should_contain('First step')
    shared_screen.should_not_contain('Second step')

    shared_screen.click('Next')
    shared_screen.should_contain('Second step')
    shared_screen.should_not_contain('First step')

    shared_screen.click('Back')
    shared_screen.should_contain('First step')
    shared_screen.should_not_contain('Second step')
