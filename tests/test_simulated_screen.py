import asyncio

import pytest
from fastapi.responses import PlainTextResponse

from nicegui import app, ui
from nicegui.testing import User

# pylint: disable=missing-function-docstring


async def test_auto_index_page(user: User) -> None:
    ui.label('Main page')

    await user.open('/')
    await user.should_see(content='Main page')


async def test_multiple_pages(create_user) -> None:
    @ui.page('/')
    def index():
        ui.label('Main page')

    @ui.page('/other')
    def other():
        ui.label('Other page')

    userA = create_user()
    userB = create_user()

    await userA.open('/')
    await userA.should_see(content='Main page')
    await userB.open('/other')
    await userB.should_see(content='Other page')
    userA.activate()
    await userA.should_see(content='Main page')
    userB.activate()
    await userB.should_see(content='Other page')


async def test_source_element(user: User) -> None:
    @ui.page('/')
    def index():
        ui.image('https://via.placeholder.com/150')

    await user.open('/')
    await user.should_see(content='placeholder.com')


async def test_button_click(user: User) -> None:
    @ui.page('/')
    def index():
        ui.button('click me', on_click=lambda: ui.label('clicked'))

    await user.open('/')
    await user.click(content='click me')
    await user.should_see(content='clicked')


async def test_assertion_raised_when_non_nicegui_page_is_returned(user: User) -> None:
    @app.get('/plain')
    def index() -> PlainTextResponse:
        return PlainTextResponse('Hello')

    with pytest.raises(ValueError):
        await user.open('/plain')


async def test_assertion_raised_when_element_not_found(user: User) -> None:
    @ui.page('/')
    def index():
        ui.label('Hello')

    await user.open('/')
    with pytest.raises(AssertionError):
        await user.should_see(content='World')


@pytest.mark.parametrize('storage_builder', [lambda:app.storage.browser, lambda:app.storage.user])
async def test_storage(user: User, storage_builder) -> None:
    @ui.page('/')
    def page():
        storage = storage_builder()
        storage['count'] = storage.get('count', 0) + 1
        ui.label().bind_text_from(storage, 'count')

    await user.open('/')
    await user.should_see(content='1')

    await user.open('/')
    await user.should_see(content='2')


async def test_navigation(user: User) -> None:
    @ui.page('/')
    def page():
        ui.label('Main page')
        ui.button('go to', on_click=lambda: ui.navigate.to('/other'))
        ui.button('forward', on_click=ui.navigate.forward)

    @ui.page('/other')
    def other():
        ui.label('Other page')
        ui.button('back', on_click=ui.navigate.back)

    await user.open('/')
    await user.should_see(content='Main page')
    await user.click(content='go to')
    await asyncio.sleep(1)
    await user.should_see(content='Other page')


async def test_notification(user: User) -> None:
    @ui.page('/')
    def page():
        ui.button('notify', on_click=lambda: ui.notify('Hello'))

    await user.open('/')
    await user.click(content='notify')
    await user.should_see(content='Hello')


async def test_checkbox(user: User) -> None:
    checkbox = ui.checkbox('my checkbox', on_change=lambda e: ui.notify(f'Changed: {e.value}'))
    ui.label().bind_text_from(checkbox, 'value', lambda v: 'enabled' if v else 'disabled')

    await user.open('/')
    await user.should_see(content='disabled')
    await user.click(content='checkbox')
    await user.should_see(content='enabled')
    await user.should_see(content='Changed: True')
    await user.click(content='checkbox')
    await user.should_see(content='disabled')
    await user.should_see(content='Changed: False')
