import asyncio

import pytest

from nicegui import core
from nicegui.awaitable_response import AwaitableResponse, NullResponse


@pytest.mark.parametrize('with_fire_and_forget', [True, False])
async def test_awaitable_response(with_fire_and_forget: bool):
    core.loop = asyncio.get_event_loop()
    actions = []

    def do_something() -> AwaitableResponse:
        def fire_and_forget():
            actions.append('fire_and_forget')

        async def wait_for_result() -> str:
            actions.append('wait_for_result')
            return 'result'

        return AwaitableResponse(fire_and_forget if with_fire_and_forget else None, wait_for_result)

    fired = ['fire_and_forget'] if with_fire_and_forget else []
    actions.clear()
    do_something()
    await asyncio.sleep(0.1)
    assert actions == fired

    actions.clear()
    result = await do_something()
    assert result == 'result'
    assert actions == ['wait_for_result']

    actions.clear()
    result = do_something()
    await asyncio.sleep(0.1)
    with pytest.raises(RuntimeError, match='AwaitableResponse must be awaited immediately after creation or not at all'):
        await result
    assert actions == fired


async def test_null_response():
    NullResponse()

    core.loop = asyncio.get_event_loop()
    await NullResponse()
