import asyncio

import pytest

from nicegui import Event, app, ui
from nicegui.testing import User


async def test_event(user: User):
    event = Event()

    @ui.page('/')
    def page():
        ui.button('Click me', on_click=event.emit)
        event.subscribe(lambda: ui.notify('clicked'))

    await user.open('/')
    user.find('Click me').click()
    await user.should_see('clicked')


async def test_event_with_args(user: User):
    event = Event[int]()

    @ui.page('/')
    def page():
        ui.button('Click me', on_click=lambda: event.emit(42))
        event.subscribe(lambda: ui.notify('clicked'))
        event.subscribe(lambda x: ui.notify(f'{x = }'))

    await user.open('/')
    user.find('Click me').click()
    await user.should_see('clicked')
    await user.should_see('x = 42')


async def test_event_with_async_handler(user: User):
    event = Event()

    @ui.page('/')
    def page():
        ui.button('Click me', on_click=event.emit)

        @event.subscribe
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
            event.subscribe(lambda: ui.label('clicked'))

    await user.open('/')
    user.find('Click me').click()
    assert len(card.default_slot.children) == 1


async def test_exception_during_emit(user: User, caplog: pytest.LogCaptureFixture):
    event = Event()
    event.subscribe(lambda: print(1 / 0))

    exceptions = []
    app.on_exception(exceptions.append)

    @ui.page('/')
    def page():
        ui.button('Click me', on_click=event.emit)

    await user.open('/')
    user.find('Click me').click()
    assert len(exceptions) == 1 and isinstance(exceptions[0], ZeroDivisionError)
    assert len(caplog.records) == 1 and 'division by zero' in caplog.records[0].message
    caplog.records.pop(0)


async def test_exception_during_call(user: User):
    event = Event()
    event.subscribe(lambda: print(1 / 0))

    @ui.page('/')
    def page():
        @ui.button('Click me').on_click
        async def click():
            try:
                await event.call()
            except Exception:
                ui.notify('There was an exception')

    await user.open('/')
    user.find('Click me').click()
    await user.should_see('There was an exception')
