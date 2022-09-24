import asyncio

from nicegui import ui

from .user import User


def test_adding_element_to_shared_index_page(user: User):
    ui.button('add label', on_click=lambda: ui.label('added'))

    user.open('/')
    user.click('add label')
    user.should_see('added')


def test_adding_element_to_private_page(user: User):
    @ui.page('/')
    def page():
        ui.button('add label', on_click=lambda: ui.label('added'))

    user.open('/')
    user.click('add label')
    user.should_see('added')


def test_adding_elements_with_async_await(user: User):
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

    user.open('/')
    assert '''
card
  A
card
  B
''' in user.page(), f'{user.page()} should show cards with "A" and "B"'
