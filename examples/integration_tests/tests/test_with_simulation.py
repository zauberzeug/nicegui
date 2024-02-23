
import pytest

from nicegui.testing import SimulatedScreen

from .. import main

# pylint: disable=missing-function-docstring


@pytest.mark.module_under_test(main)
async def test_markdown_message(screen: SimulatedScreen) -> None:
    with await screen.open('/') as user:
        user.should_see(content='Try running')


@pytest.mark.module_under_test(main)
async def test_button_click(screen: SimulatedScreen) -> None:
    with await screen.open('/') as user:
        user.click(content='Click me')
        user.should_see(content='Button clicked!')


@pytest.mark.module_under_test(main)
async def test_sub_page(screen: SimulatedScreen) -> None:
    with await screen.open('/subpage') as user:
        user.should_see(content='This is a subpage')


@pytest.mark.module_under_test(main)
async def test_with_connected(screen: SimulatedScreen) -> None:
    with await screen.open('/with_connected') as user:
        user.should_see(content='This is an async connection demo')
        user.should_see(content='Connected!')
