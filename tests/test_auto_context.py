import asyncio

from nicegui import ui

from .screen import Screen


def test_adding_element_to_shared_index_page(screen: Screen):
    ui.button('add label', on_click=lambda: ui.label('added'))

    screen.open('/')
    screen.click('add label')
    screen.should_contain('added')


def test_adding_element_to_private_page(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('add label', on_click=lambda: ui.label('added'))

    screen.open('/')
    screen.click('add label')
    screen.should_contain('added')


def test_adding_elements_with_async_await(screen: Screen):
    async def add_a():
        await asyncio.sleep(0.1)
        ui.label('A')

    async def add_b():
        await asyncio.sleep(0.1)
        ui.label('B')

    with ui.card():
        ui.timer(1.0, add_a, once=True)
    with ui.card():
        ui.timer(1.1, add_b, once=True)

    screen.open('/')
    for i in range(20):
        if 'card\n  A\ncard\n  B' in screen.render_content():
            return
        screen.wait(0.1)
    raise AssertionError(f'{screen.render_content()} should show cards with "A" and "B"')
