import asyncio

from nicegui import ui

from .screen import Screen


def test_refreshable(screen: Screen) -> None:
    numbers = []

    @ui.refreshable
    def number_ui() -> None:
        ui.label('[' + ', '.join(str(n) for n in sorted(numbers)) + ']')

    number_ui()
    ui.button('Refresh', on_click=number_ui.refresh)

    screen.open('/')
    screen.should_contain('[]')

    numbers.append(1)
    screen.click('Refresh')
    screen.should_contain('[1]')

    numbers.append(2)
    screen.click('Refresh')
    screen.should_contain('[1, 2]')

    numbers.clear()
    screen.click('Refresh')
    screen.should_contain('[]')


async def test_async_refreshable(screen: Screen) -> None:
    numbers = []

    @ui.refreshable
    async def number_ui() -> None:
        await asyncio.sleep(0.1)
        ui.label('[' + ', '.join(str(n) for n in sorted(numbers)) + ']')

    @ui.page('/')
    async def index():
        with ui.column():  # this is necessary to reproduce bug #863
            await number_ui()
        ui.button('Refresh', on_click=number_ui.refresh)

    screen.open('/')
    screen.should_contain('[]')

    numbers.append(1)
    screen.click('Refresh')
    screen.should_not_contain('[]')  # ensure bug #863 is fixed
    screen.should_contain('[1]')

    numbers.append(2)
    screen.click('Refresh')
    screen.should_not_contain('[]')
    screen.should_contain('[1, 2]')

    numbers.clear()
    screen.click('Refresh')
    screen.should_contain('[]')
