import pytest

import main
from nicegui.testing import SimulatedScreen

# pylint: disable=missing-function-docstring


@pytest.mark.module_under_test(main)
async def test_start_screen(screen: SimulatedScreen) -> None:
    with await screen.open('/'):
        await screen.should_contain('simple chat app')
        await screen.should_contain('https://robohash.org/')
