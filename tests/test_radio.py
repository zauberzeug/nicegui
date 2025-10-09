from nicegui import ui
from nicegui.testing import Screen, User


def test_radio_click(screen: Screen):
    @ui.page('/')
    def page():
        radio = ui.radio(['A', 'B', 'C'])
        ui.label().bind_text_from(radio, 'value', lambda x: f'Value: {x}')

    screen.open('/')
    screen.click('A')
    screen.should_contain('Value: A')
    screen.click('B')
    screen.should_contain('Value: B')

    screen.click('B')  # already selected, should not change
    screen.wait(0.5)
    screen.should_contain('Value: B')


def test_radio_set_value(screen: Screen):
    radio = None

    @ui.page('/')
    def page():
        nonlocal radio
        radio = ui.radio(['A', 'B', 'C'])
        ui.label().bind_text_from(radio, 'value', lambda x: f'Value: {x}')

    screen.open('/')
    radio.set_value('B')
    screen.should_contain('Value: B')


def test_radio_set_options(screen: Screen):
    radio = None

    @ui.page('/')
    def page():
        nonlocal radio
        radio = ui.radio(['A', 'B', 'C'], value='C', on_change=lambda e: ui.notify(f'Event: {e.value}'))
        ui.label().bind_text_from(radio, 'value', lambda x: f'Value: {x}')

        ui.button('reverse', on_click=lambda: (radio.options.reverse(), radio.update()))  # type: ignore
        ui.button('clear', on_click=lambda: (radio.options.clear(), radio.update()))  # type: ignore

    screen.open('/')
    radio.set_options(['C', 'D', 'E'])
    screen.should_contain('D')
    screen.should_contain('E')
    screen.should_contain('Value: C')

    radio.set_options(['X', 'Y', 'Z'])
    screen.should_contain('X')
    screen.should_contain('Y')
    screen.should_contain('Z')
    screen.should_contain('Value: None')
    screen.should_contain('Event: None')

    radio.set_options(['1', '2', '3'], value='3')
    screen.should_contain('Value: 3')
    screen.should_contain('Event: 3')

    screen.click('reverse')
    screen.should_contain('Value: 3')
    screen.should_contain('Event: 3')

    screen.click('clear')
    screen.should_contain('Value: None')


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
