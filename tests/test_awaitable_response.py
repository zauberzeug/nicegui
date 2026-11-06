import asyncio

import pytest

from nicegui import core
from nicegui.awaitable_response import AwaitableResponse, NullResponse


async def test_awaitable_response():
    core.loop = asyncio.get_event_loop()
    actions = []

    def do_something() -> AwaitableResponse:
        def fire_and_forget():
            actions.append('fire_and_forget')

        async def wait_for_result() -> str:
            actions.append('wait_for_result')
            return 'result'

        return AwaitableResponse(fire_and_forget, wait_for_result)

    actions.clear()
    do_something()
    await asyncio.sleep(0.1)
    assert actions == ['fire_and_forget']

    actions.clear()
    result = await do_something()
    assert result == 'result'
    assert actions == ['wait_for_result']

    actions.clear()
    result = do_something()
    await asyncio.sleep(0.1)
    with pytest.raises(RuntimeError, match='AwaitableResponse must be awaited immediately after creation or not at all'):
        await result
    assert actions == ['fire_and_forget']


async def test_null_response():
    NullResponse()

    core.loop = asyncio.get_event_loop()
    await NullResponse()
