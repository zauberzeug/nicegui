from nicegui import ui
from nicegui.testing import Screen, User


def test_stepper(screen: Screen):
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

    screen.open('/')
    screen.should_contain('First step')
    screen.should_not_contain('Second step')

    screen.click('Next')
    screen.should_contain('Second step')
    screen.should_not_contain('First step')

    screen.click('Back')
    screen.should_contain('First step')
    screen.should_not_contain('Second step')


async def test_done_decoration_with_step_object(user: User):
    stepper = step_three = None

    @ui.page('/')
    def page():
        nonlocal stepper, step_three
        with ui.stepper() as stepper:
            ui.step('one')
            ui.step('two')
            step_three = ui.step('three')

    await user.open('/')
    stepper.value = step_three
    assert [step.props.get(':done') for step in stepper] == ['True', 'True', 'False']
