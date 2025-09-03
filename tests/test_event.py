import asyncio

from nicegui import Event, ui
from nicegui.testing import User


async def test_event(user: User):
    event = Event()

    @ui.page('/')
    def page():
        ui.button('Click me', on_click=event.emit)
        event.subscribe_ui(lambda: ui.notify('clicked'))

    await user.open('/')
    user.find('Click me').click()
    await user.should_see('clicked')


async def test_event_with_args(user: User):
    event = Event[int]()

    @ui.page('/')
    def page():
        ui.button('Click me', on_click=lambda: event.emit(42))
        event.subscribe_ui(lambda: ui.notify('clicked'))
        event.subscribe_ui(lambda x: ui.notify(f'{x = }'))

    await user.open('/')
    user.find('Click me').click()
    await user.should_see('clicked')
    await user.should_see('x = 42')


async def test_event_with_async_handler(user: User):
    event = Event()

    @ui.page('/')
    def page():
        ui.button('Click me', on_click=event.emit)

        @event.subscribe_ui
        async def handler():
            await asyncio.sleep(0.1)
            ui.notify('clicked')

    await user.open('/')
    user.find('Click me').click()
    await user.should_see('clicked')


async def test_event_handler_in_correct_slot(user: User):
    event = Event()
    card = None

    @ui.page('/')
    def page():
        nonlocal card
        ui.button('Click me', on_click=event.emit)
        with ui.card() as card:
            event.subscribe_ui(lambda: ui.label('clicked'))

    await user.open('/')
    user.find('Click me').click()
    assert len(card.default_slot.children) == 1
