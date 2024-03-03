import asyncio

import pytest
from fastapi.responses import PlainTextResponse

from nicegui import ElementFilter, app, ui
from nicegui.testing import SimulatedScreen

# pylint: disable=missing-function-docstring


async def test_multiple_pages(screen: SimulatedScreen) -> None:
    @ui.page('/')
    def index():
        ui.label('Main page')

    @ui.page('/other')
    def other():
        ui.label('Other page')

    with await screen.open('/') as userA:
        await userA.should_see(content='Main page')
    with await screen.open('/other') as userB:
        await userB.should_see(content='Other page')
    with userA:
        await userA.should_see(content='Main page')
    with userB:
        await userB.should_see(content='Other page')


async def test_source_element(screen: SimulatedScreen) -> None:
    @ui.page('/')
    def index():
        ui.image('https://via.placeholder.com/150')

    with await screen.open('/') as user:
        await user.should_see(content='placeholder.com')


async def test_assertion_raised_when_non_nicegui_page_is_returned(screen: SimulatedScreen) -> None:
    @app.get('/plain')
    def index() -> PlainTextResponse:
        return PlainTextResponse('Hello')

    with pytest.raises(ValueError):
        await screen.open('/plain')


async def test_assertion_raised_when_element_not_found(screen: SimulatedScreen) -> None:
    @ui.page('/')
    def index():
        ui.label('Hello')

    with await screen.open('/') as user:
        with pytest.raises(AssertionError):
            await user.should_see(content='World')


@pytest.mark.parametrize('storage_builder', [lambda:app.storage.browser, lambda:app.storage.user])
async def test_storage(screen: SimulatedScreen, storage_builder) -> None:
    @ui.page('/')
    def page():
        storage = storage_builder()
        storage['count'] = storage.get('count', 0) + 1
        ui.label().bind_text_from(storage, 'count')

    with await screen.open('/') as user:
        await user.should_see(content='1')

    with await screen.open('/') as user:
        await user.should_see(content='2')
