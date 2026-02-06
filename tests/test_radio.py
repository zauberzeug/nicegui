from nicegui import ui
from nicegui.testing import SharedScreen, User


def test_radio_click(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        radio = ui.radio(['A', 'B', 'C'])
        ui.label().bind_text_from(radio, 'value', lambda x: f'Value: {x}')

    shared_screen.open('/')
    shared_screen.click('A')
    shared_screen.should_contain('Value: A')
    shared_screen.click('B')
    shared_screen.should_contain('Value: B')

    shared_screen.click('B')  # already selected, should not change
    shared_screen.wait(0.5)
    shared_screen.should_contain('Value: B')


def test_radio_set_value(shared_screen: SharedScreen):
    radio = None

    @ui.page('/')
    def page():
        nonlocal radio
        radio = ui.radio(['A', 'B', 'C'])
        ui.label().bind_text_from(radio, 'value', lambda x: f'Value: {x}')

    shared_screen.open('/')
    radio.set_value('B')
    shared_screen.should_contain('Value: B')


def test_radio_set_options(shared_screen: SharedScreen):
    radio = None

    @ui.page('/')
    def page():
        nonlocal radio
        radio = ui.radio(['A', 'B', 'C'], value='C', on_change=lambda e: ui.notify(f'Event: {e.value}'))
        ui.label().bind_text_from(radio, 'value', lambda x: f'Value: {x}')

        ui.button('reverse', on_click=lambda: (radio.options.reverse(), radio.update()))  # type: ignore
        ui.button('clear', on_click=lambda: (radio.options.clear(), radio.update()))  # type: ignore

    shared_screen.open('/')
    radio.set_options(['C', 'D', 'E'])
    shared_screen.should_contain('D')
    shared_screen.should_contain('E')
    shared_screen.should_contain('Value: C')

    radio.set_options(['X', 'Y', 'Z'])
    shared_screen.should_contain('X')
    shared_screen.should_contain('Y')
    shared_screen.should_contain('Z')
    shared_screen.should_contain('Value: None')
    shared_screen.should_contain('Event: None')

    radio.set_options(['1', '2', '3'], value='3')
    shared_screen.should_contain('Value: 3')
    shared_screen.should_contain('Event: 3')

    shared_screen.click('reverse')
    shared_screen.should_contain('Value: 3')
    shared_screen.should_contain('Event: 3')

    shared_screen.click('clear')
    shared_screen.should_contain('Value: None')


async def test_radio_click_with_user(user: User):
    @ui.page('/')
    def page():
        radio = ui.radio(['A', 'B', 'C'])
        ui.label().bind_text_from(radio, 'value', lambda x: f'Value: {x}')

    await user.open('/')
    user.find('A', kind=ui.radio).click()
    await user.should_see('Value: A')

    user.find('B', kind=ui.radio).click()
    await user.should_see('Value: B')

    user.find('B', kind=ui.radio).click()  # already selected, should not change
    await user.should_see('Value: B')
